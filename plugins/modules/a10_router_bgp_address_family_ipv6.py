#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Copyright 2018 A10 Networks
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

REQUIRED_NOT_SET = (False, "One of ({}) must be set.")
REQUIRED_MUTEX = (False, "Only one of ({}) can be set.")
REQUIRED_VALID = (True, "")

DOCUMENTATION = r'''
module: a10_router_bgp_address_family_ipv6
description:
    - ipv6 Address family
short_description: Configures A10 router.bgp.address.family.ipv6
author: A10 Networks 2018
version_added: 2.4
options:
    state:
        description:
        - State of the object to be created.
        choices:
          - noop
          - present
        required: True
    ansible_host:
        description:
        - Host for AXAPI authentication
        required: True
    ansible_username:
        description:
        - Username for AXAPI authentication
        required: True
    ansible_password:
        description:
        - Password for AXAPI authentication
        required: True
    ansible_port:
        description:
        - Port for AXAPI authentication
        required: True
    a10_device_context_id:
        description:
        - Device ID for aVCS configuration
        choices: [1-8]
        required: False
    a10_partition:
        description:
        - Destination/target partition for object/command
        required: False
    bgp_as_number:
        description:
        - Key to identify parent object    distance:
        description:
        - "Field distance"
        required: False
        suboptions:
            distance_ext:
                description:
                - "Distance for routes external to the AS"
            distance_local:
                description:
                - "Distance for local routes"
            distance_int:
                description:
                - "Distance for routes internal to the AS"
    redistribute:
        description:
        - "Field redistribute"
        required: False
        suboptions:
            ip_nat_list_cfg:
                description:
                - "Field ip_nat_list_cfg"
            lw4o6_cfg:
                description:
                - "Field lw4o6_cfg"
            nat64_cfg:
                description:
                - "Field nat64_cfg"
            uuid:
                description:
                - "uuid of the object"
            connected_cfg:
                description:
                - "Field connected_cfg"
            ip_nat_cfg:
                description:
                - "Field ip_nat_cfg"
            floating_ip_cfg:
                description:
                - "Field floating_ip_cfg"
            isis_cfg:
                description:
                - "Field isis_cfg"
            vip:
                description:
                - "Field vip"
            rip_cfg:
                description:
                - "Field rip_cfg"
            ospf_cfg:
                description:
                - "Field ospf_cfg"
            static_cfg:
                description:
                - "Field static_cfg"
            nat_map_cfg:
                description:
                - "Field nat_map_cfg"
    aggregate_address_list:
        description:
        - "Field aggregate_address_list"
        required: False
        suboptions:
            as_set:
                description:
                - "Generate AS set path information"
            aggregate_address:
                description:
                - "Configure BGP aggregate entries (Aggregate IPv6 prefix)"
            summary_only:
                description:
                - "Filter more specific routes from updates"
    originate:
        description:
        - "Distribute an IPv6 default route"
        required: False
    maximum_paths_value:
        description:
        - "Supported BGP multipath numbers"
        required: False
    bgp:
        description:
        - "Field bgp"
        required: False
        suboptions:
            dampening_max_supress:
                description:
                - "Maximum duration to suppress a stable route(minutes)"
            dampening:
                description:
                - "Enable route-flap dampening"
            dampening_half:
                description:
                - "Reachability Half-life time for the penalty(minutes)"
            dampening_start_reuse:
                description:
                - "Value to start reusing a route"
            route_map:
                description:
                - "Route-map to specify criteria for dampening (Route-map name)"
            dampening_start_supress:
                description:
                - "Value to start suppressing a route"
            dampening_unreachability:
                description:
                - "Un-reachability Half-life time for the penalty(minutes)"
    auto_summary:
        description:
        - "Enable automatic network number summarization"
        required: False
    synchronization:
        description:
        - "Perform IGP synchronization"
        required: False
    neighbor:
        description:
        - "Field neighbor"
        required: False
        suboptions:
            peer_group_neighbor_list:
                description:
                - "Field peer_group_neighbor_list"
            ipv6_neighbor_list:
                description:
                - "Field ipv6_neighbor_list"
            ipv4_neighbor_list:
                description:
                - "Field ipv4_neighbor_list"
    uuid:
        description:
        - "uuid of the object"
        required: False
    network:
        description:
        - "Field network"
        required: False
        suboptions:
            ipv6_network_list:
                description:
                - "Field ipv6_network_list"
            synchronization:
                description:
                - "Field synchronization"

'''

EXAMPLES = """
"""

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'supported_by': 'community',
    'status': ['preview']
}

# Hacky way of having access to object properties for evaluation
AVAILABLE_PROPERTIES = [
    "aggregate_address_list",
    "auto_summary",
    "bgp",
    "distance",
    "maximum_paths_value",
    "neighbor",
    "network",
    "originate",
    "redistribute",
    "synchronization",
    "uuid",
]

from ansible_collections.a10.acos_axapi.plugins.module_utils import \
    errors as a10_ex
from ansible_collections.a10.acos_axapi.plugins.module_utils.axapi_http import \
    client_factory
from ansible_collections.a10.acos_axapi.plugins.module_utils.kwbl import \
    KW_OUT, translate_blacklist as translateBlacklist


def get_default_argspec():
    return dict(
        ansible_host=dict(type='str', required=True),
        ansible_username=dict(type='str', required=True),
        ansible_password=dict(type='str', required=True, no_log=True),
        state=dict(type='str', default="present", choices=['noop', 'present']),
        ansible_port=dict(type='int', choices=[80, 443], required=True),
        a10_partition=dict(
            type='dict',
            name=dict(type='str', ),
            shared=dict(type='str', ),
            required=False,
        ),
        a10_device_context_id=dict(
            type='int',
            choices=[1, 2, 3, 4, 5, 6, 7, 8],
            required=False,
        ),
        get_type=dict(type='str', choices=["single", "list", "oper", "stats"]),
    )


def get_argspec():
    rv = get_default_argspec()
    rv.update({
        'distance': {
            'type': 'dict',
            'distance_ext': {
                'type': 'int',
            },
            'distance_local': {
                'type': 'int',
            },
            'distance_int': {
                'type': 'int',
            }
        },
        'redistribute': {
            'type': 'dict',
            'ip_nat_list_cfg': {
                'type': 'dict',
                'ip_nat_list': {
                    'type': 'bool',
                },
                'route_map': {
                    'type': 'str',
                }
            },
            'lw4o6_cfg': {
                'type': 'dict',
                'route_map': {
                    'type': 'str',
                },
                'lw4o6': {
                    'type': 'bool',
                }
            },
            'nat64_cfg': {
                'type': 'dict',
                'nat64': {
                    'type': 'bool',
                },
                'route_map': {
                    'type': 'str',
                }
            },
            'uuid': {
                'type': 'str',
            },
            'connected_cfg': {
                'type': 'dict',
                'route_map': {
                    'type': 'str',
                },
                'connected': {
                    'type': 'bool',
                }
            },
            'ip_nat_cfg': {
                'type': 'dict',
                'route_map': {
                    'type': 'str',
                },
                'ip_nat': {
                    'type': 'bool',
                }
            },
            'floating_ip_cfg': {
                'type': 'dict',
                'floating_ip': {
                    'type': 'bool',
                },
                'route_map': {
                    'type': 'str',
                }
            },
            'isis_cfg': {
                'type': 'dict',
                'route_map': {
                    'type': 'str',
                },
                'isis': {
                    'type': 'bool',
                }
            },
            'vip': {
                'type': 'dict',
                'only_not_flagged_cfg': {
                    'type': 'dict',
                    'route_map': {
                        'type': 'str',
                    },
                    'only_not_flagged': {
                        'type': 'bool',
                    }
                },
                'only_flagged_cfg': {
                    'type': 'dict',
                    'route_map': {
                        'type': 'str',
                    },
                    'only_flagged': {
                        'type': 'bool',
                    }
                }
            },
            'rip_cfg': {
                'type': 'dict',
                'route_map': {
                    'type': 'str',
                },
                'rip': {
                    'type': 'bool',
                }
            },
            'ospf_cfg': {
                'type': 'dict',
                'route_map': {
                    'type': 'str',
                },
                'ospf': {
                    'type': 'bool',
                }
            },
            'static_cfg': {
                'type': 'dict',
                'route_map': {
                    'type': 'str',
                },
                'static': {
                    'type': 'bool',
                }
            },
            'nat_map_cfg': {
                'type': 'dict',
                'route_map': {
                    'type': 'str',
                },
                'nat_map': {
                    'type': 'bool',
                }
            }
        },
        'aggregate_address_list': {
            'type': 'list',
            'as_set': {
                'type': 'bool',
            },
            'aggregate_address': {
                'type': 'str',
            },
            'summary_only': {
                'type': 'bool',
            }
        },
        'originate': {
            'type': 'bool',
        },
        'maximum_paths_value': {
            'type': 'int',
        },
        'bgp': {
            'type': 'dict',
            'dampening_max_supress': {
                'type': 'int',
            },
            'dampening': {
                'type': 'bool',
            },
            'dampening_half': {
                'type': 'int',
            },
            'dampening_start_reuse': {
                'type': 'int',
            },
            'route_map': {
                'type': 'str',
            },
            'dampening_start_supress': {
                'type': 'int',
            },
            'dampening_unreachability': {
                'type': 'int',
            }
        },
        'auto_summary': {
            'type': 'bool',
        },
        'synchronization': {
            'type': 'bool',
        },
        'neighbor': {
            'type': 'dict',
            'peer_group_neighbor_list': {
                'type': 'list',
                'maximum_prefix': {
                    'type': 'int',
                },
                'neighbor_prefix_lists': {
                    'type': 'list',
                    'nbr_prefix_list_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    },
                    'nbr_prefix_list': {
                        'type': 'str',
                    }
                },
                'activate': {
                    'type': 'bool',
                },
                'weight': {
                    'type': 'int',
                },
                'send_community_val': {
                    'type': 'str',
                    'choices': ['both', 'none', 'standard', 'extended']
                },
                'inbound': {
                    'type': 'bool',
                },
                'next_hop_self': {
                    'type': 'bool',
                },
                'maximum_prefix_thres': {
                    'type': 'int',
                },
                'route_map': {
                    'type': 'str',
                },
                'peer_group': {
                    'type': 'str',
                    'required': True,
                },
                'remove_private_as': {
                    'type': 'bool',
                },
                'default_originate': {
                    'type': 'bool',
                },
                'allowas_in_count': {
                    'type': 'int',
                },
                'distribute_lists': {
                    'type': 'list',
                    'distribute_list_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    },
                    'distribute_list': {
                        'type': 'str',
                    }
                },
                'prefix_list_direction': {
                    'type': 'str',
                    'choices': ['both', 'receive', 'send']
                },
                'allowas_in': {
                    'type': 'bool',
                },
                'unsuppress_map': {
                    'type': 'str',
                },
                'neighbor_filter_lists': {
                    'type': 'list',
                    'filter_list': {
                        'type': 'str',
                    },
                    'filter_list_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    }
                },
                'neighbor_route_map_lists': {
                    'type': 'list',
                    'nbr_rmap_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    },
                    'nbr_route_map': {
                        'type': 'str',
                    }
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'ipv6_neighbor_list': {
                'type': 'list',
                'maximum_prefix': {
                    'type': 'int',
                },
                'neighbor_prefix_lists': {
                    'type': 'list',
                    'nbr_prefix_list_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    },
                    'nbr_prefix_list': {
                        'type': 'str',
                    }
                },
                'allowas_in_count': {
                    'type': 'int',
                },
                'neighbor_ipv6': {
                    'type': 'str',
                    'required': True,
                },
                'send_community_val': {
                    'type': 'str',
                    'choices': ['both', 'none', 'standard', 'extended']
                },
                'inbound': {
                    'type': 'bool',
                },
                'next_hop_self': {
                    'type': 'bool',
                },
                'maximum_prefix_thres': {
                    'type': 'int',
                },
                'route_map': {
                    'type': 'str',
                },
                'peer_group_name': {
                    'type': 'str',
                },
                'weight': {
                    'type': 'int',
                },
                'unsuppress_map': {
                    'type': 'str',
                },
                'prefix_list_direction': {
                    'type': 'str',
                    'choices': ['both', 'receive', 'send']
                },
                'default_originate': {
                    'type': 'bool',
                },
                'activate': {
                    'type': 'bool',
                },
                'remove_private_as': {
                    'type': 'bool',
                },
                'distribute_lists': {
                    'type': 'list',
                    'distribute_list_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    },
                    'distribute_list': {
                        'type': 'str',
                    }
                },
                'allowas_in': {
                    'type': 'bool',
                },
                'neighbor_route_map_lists': {
                    'type': 'list',
                    'nbr_rmap_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    },
                    'nbr_route_map': {
                        'type': 'str',
                    }
                },
                'neighbor_filter_lists': {
                    'type': 'list',
                    'filter_list': {
                        'type': 'str',
                    },
                    'filter_list_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    }
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'ipv4_neighbor_list': {
                'type': 'list',
                'maximum_prefix': {
                    'type': 'int',
                },
                'neighbor_prefix_lists': {
                    'type': 'list',
                    'nbr_prefix_list_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    },
                    'nbr_prefix_list': {
                        'type': 'str',
                    }
                },
                'allowas_in_count': {
                    'type': 'int',
                },
                'peer_group_name': {
                    'type': 'str',
                },
                'send_community_val': {
                    'type': 'str',
                    'choices': ['both', 'none', 'standard', 'extended']
                },
                'neighbor_ipv4': {
                    'type': 'str',
                    'required': True,
                },
                'inbound': {
                    'type': 'bool',
                },
                'next_hop_self': {
                    'type': 'bool',
                },
                'maximum_prefix_thres': {
                    'type': 'int',
                },
                'route_map': {
                    'type': 'str',
                },
                'uuid': {
                    'type': 'str',
                },
                'weight': {
                    'type': 'int',
                },
                'unsuppress_map': {
                    'type': 'str',
                },
                'default_originate': {
                    'type': 'bool',
                },
                'activate': {
                    'type': 'bool',
                },
                'remove_private_as': {
                    'type': 'bool',
                },
                'prefix_list_direction': {
                    'type': 'str',
                    'choices': ['both', 'receive', 'send']
                },
                'allowas_in': {
                    'type': 'bool',
                },
                'neighbor_route_map_lists': {
                    'type': 'list',
                    'nbr_rmap_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    },
                    'nbr_route_map': {
                        'type': 'str',
                    }
                },
                'neighbor_filter_lists': {
                    'type': 'list',
                    'filter_list': {
                        'type': 'str',
                    },
                    'filter_list_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    }
                },
                'distribute_lists': {
                    'type': 'list',
                    'distribute_list_direction': {
                        'type': 'str',
                        'choices': ['in', 'out']
                    },
                    'distribute_list': {
                        'type': 'str',
                    }
                }
            }
        },
        'uuid': {
            'type': 'str',
        },
        'network': {
            'type': 'dict',
            'ipv6_network_list': {
                'type': 'list',
                'description': {
                    'type': 'str',
                },
                'route_map': {
                    'type': 'str',
                },
                'comm_value': {
                    'type': 'str',
                },
                'network_ipv6': {
                    'type': 'str',
                    'required': True,
                },
                'backdoor': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            },
            'synchronization': {
                'type': 'dict',
                'network_synchronization': {
                    'type': 'bool',
                },
                'uuid': {
                    'type': 'str',
                }
            }
        }
    })
    # Parent keys
    rv.update(dict(bgp_as_number=dict(type='str', required=True), ))
    return rv


def existing_url(module):
    """Return the URL for an existing resource"""
    # Build the format dictionary
    url_base = "/axapi/v3/router/bgp/{bgp_as_number}/address-family/ipv6"

    f_dict = {}
    f_dict["bgp_as_number"] = module.params["bgp_as_number"]

    return url_base.format(**f_dict)


def list_url(module):
    """Return the URL for a list of resources"""
    ret = existing_url(module)
    return ret[0:ret.rfind('/')]


def get(module):
    return module.client.get(existing_url(module))


def get_list(module):
    return module.client.get(list_url(module))


def exists(module):
    try:
        return get(module)
    except a10_ex.NotFound:
        return None


def _to_axapi(key):
    return translateBlacklist(key, KW_OUT).replace("_", "-")


def _build_dict_from_param(param):
    rv = {}

    for k, v in param.items():
        hk = _to_axapi(k)
        if isinstance(v, dict):
            v_dict = _build_dict_from_param(v)
            rv[hk] = v_dict
        elif isinstance(v, list):
            nv = [_build_dict_from_param(x) for x in v]
            rv[hk] = nv
        else:
            rv[hk] = v

    return rv


def build_envelope(title, data):
    return {title: data}


def new_url(module):
    """Return the URL for creating a resource"""
    # To create the URL, we need to take the format string and return it with no params
    url_base = "/axapi/v3/router/bgp/{bgp_as_number}/address-family/ipv6"

    f_dict = {}
    f_dict["bgp_as_number"] = module.params["bgp_as_number"]

    return url_base.format(**f_dict)


def validate(params):
    # Ensure that params contains all the keys.
    requires_one_of = sorted([])
    present_keys = sorted([
        x for x in requires_one_of if x in params and params.get(x) is not None
    ])

    errors = []
    marg = []

    if not len(requires_one_of):
        return REQUIRED_VALID

    if len(present_keys) == 0:
        rc, msg = REQUIRED_NOT_SET
        marg = requires_one_of
    elif requires_one_of == present_keys:
        rc, msg = REQUIRED_MUTEX
        marg = present_keys
    else:
        rc, msg = REQUIRED_VALID

    if not rc:
        errors.append(msg.format(", ".join(marg)))

    return rc, errors


def build_json(title, module):
    rv = {}

    for x in AVAILABLE_PROPERTIES:
        v = module.params.get(x)
        if v is not None:
            rx = _to_axapi(x)

            if isinstance(v, dict):
                nv = _build_dict_from_param(v)
                rv[rx] = nv
            elif isinstance(v, list):
                nv = [_build_dict_from_param(x) for x in v]
                rv[rx] = nv
            else:
                rv[rx] = module.params[x]

    return build_envelope(title, rv)


def report_changes(module, result, existing_config, payload):
    if existing_config:
        for k, v in payload["ipv6"].items():
            if isinstance(v, str):
                if v.lower() == "true":
                    v = 1
                else:
                    if v.lower() == "false":
                        v = 0
            elif k not in payload:
                break
            else:
                if existing_config["ipv6"][k] != v:
                    if result["changed"] is not True:
                        result["changed"] = True
                    existing_config["ipv6"][k] = v
            result.update(**existing_config)
    else:
        result.update(**payload)
    return result


def create(module, result, payload):
    try:
        post_result = module.client.post(new_url(module), payload)
        if post_result:
            result.update(**post_result)
        result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def update(module, result, existing_config, payload):
    try:
        post_result = module.client.post(existing_url(module), payload)
        if post_result:
            result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def present(module, result, existing_config):
    payload = build_json("ipv6", module)
    changed_config = report_changes(module, result, existing_config, payload)
    if module.check_mode:
        return changed_config
    elif not existing_config:
        return create(module, result, payload)
    elif existing_config and not changed_config.get('changed'):
        return update(module, result, existing_config, payload)
    else:
        result["changed"] = True
        return result


def replace(module, result, existing_config, payload):
    try:
        post_result = module.client.put(existing_url(module), payload)
        if post_result:
            result.update(**post_result)
        if post_result == existing_config:
            result["changed"] = False
        else:
            result["changed"] = True
    except a10_ex.ACOSException as ex:
        module.fail_json(msg=ex.msg, **result)
    except Exception as gex:
        raise gex
    return result


def run_command(module):
    run_errors = []

    result = dict(changed=False, original_message="", message="", result={})

    state = module.params["state"]
    ansible_host = module.params["ansible_host"]
    ansible_username = module.params["ansible_username"]
    ansible_password = module.params["ansible_password"]
    ansible_port = module.params["ansible_port"]
    a10_partition = module.params["a10_partition"]
    a10_device_context_id = module.params["a10_device_context_id"]

    if ansible_port == 80:
        protocol = "http"
    elif ansible_port == 443:
        protocol = "https"

    valid = True

    if state == 'present':
        valid, validation_errors = validate(module.params)
        for ve in validation_errors:
            run_errors.append(ve)

    if not valid:
        err_msg = "\n".join(run_errors)
        result["messages"] = "Validation failure: " + str(run_errors)
        module.fail_json(msg=err_msg, **result)

    module.client = client_factory(ansible_host, ansible_port, protocol,
                                   ansible_username, ansible_password)

    if a10_partition:
        module.client.activate_partition(a10_partition)

    if a10_device_context_id:
        module.client.change_context(a10_device_context_id)

    existing_config = exists(module)

    if state == 'present':
        result = present(module, result, existing_config)

    if state == 'noop':
        if module.params.get("get_type") == "single":
            result["result"] = get(module)
        elif module.params.get("get_type") == "list":
            result["result"] = get_list(module)
    module.client.session.close()
    return result


def main():
    module = AnsibleModule(argument_spec=get_argspec(),
                           supports_check_mode=True)
    result = run_command(module)
    module.exit_json(**result)


# standard ansible module imports
from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
    main()
