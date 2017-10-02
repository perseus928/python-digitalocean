# -*- coding: utf-8 -*-
from .baseapi import BaseAPI, POST, DELETE, PUT
import jsonpickle


class _targets(object):
    """
    An internal object that both `Sources` and `Destinations` derive from.

    Not for direct use by end users.
    """
    def __init__(self, addresses=[], droplet_ids=[],
                 load_balancer_uids=[], tags=[]):
        self.addresses = addresses
        self.droplet_ids = droplet_ids
        self.load_balancer_uids = load_balancer_uids
        self.tags = tags


class Sources(_targets):
    """
    An object holding information about an InboundRule's sources.

    Args:
        addresses (obj:`list`): An array of strings containing the IPv4
            addresses, IPv6 addresses, IPv4 CIDRs, and/or IPv6 CIDRs to which
            the Firewall will allow traffic.
        droplet_ids (obj:`list`): An array containing the IDs of the Droplets
            to which the Firewall will allow traffic.
        load_balancer_uids (obj:`list`): An array containing the IDs of the
            Load Balancers to which the Firewall will allow traffic.
        tags (obj:`list`): An array containing the names of Tags corresponding
            to groups of Droplets to which the Firewall will allow traffic.
    """
    pass


class Destinations(_targets):
    """
    An object holding information about an OutboundRule's destinations.

    Args:
        addresses (obj:`list`): An array of strings containing the IPv4
            addresses, IPv6 addresses, IPv4 CIDRs, and/or IPv6 CIDRs to which
            the Firewall will allow traffic.
        droplet_ids (obj:`list`): An array containing the IDs of the Droplets
            to which the Firewall will allow traffic.
        load_balancer_uids (obj:`list`): An array containing the IDs of the
            Load Balancers to which the Firewall will allow traffic.
        tags (obj:`list`): An array containing the names of Tags corresponding
            to groups of Droplets to which the Firewall will allow traffic.
    """
    pass


class InboundRule(object):
    """
    An object holding information about a Firewall's inbound rule.

    Args:
        protocol (str): The type of traffic to be allowed. This may be one
            of "tcp", "udp", or "icmp".
        port (str): The ports on which traffic will be allowed specified as a
            string containing a single port, a range (e.g. "8000-9000"), or
            "all" to open all ports for a protocol.
        sources (obj): A `Sources` object.
    """
    def __init__(self, protocol="", ports="", sources=""):
        self.protocol = protocol
        self.ports = ports

        if isinstance(sources, Sources):
            self.sources = sources
        else:
            for source in sources:
                self.sources = Sources(**sources)


class OutboundRule(object):
    """
    An object holding information about a Firewall's outbound rule.

    Args:
        protocol (str): The type of traffic to be allowed. This may be one
            of "tcp", "udp", or "icmp".
        port (str): The ports on which traffic will be allowed specified as a
            string containing a single port, a range (e.g. "8000-9000"), or
            "all" to open all ports for a protocol.
        destinations (obj): A `Destinations` object.
    """
    def __init__(self, protocol="", ports="", destinations=""):
        self.protocol = protocol
        self.ports = ports

        if isinstance(destinations, Destinations):
            self.destinations = destinations
        else:
            for destination in destinations:
                self.destinations = Destinations(**destinations)


class Firewall(BaseAPI):
    """
    An object representing an DigitalOcean Firewall.

    Attributes accepted at creation time:

    Args:
        name (str): The Firewall's name.
        droplet_ids (obj:`list` of `int`): A list of Droplet IDs to be assigned
            to the Firewall.
        tags (obj:`list` of `str`):  A list Tag names to be assigned to the
            Firewall.
        inbound_rules (obj:`list`): A list of `InboundRules` objects
        outbound_rules (obj:`list`): A list of `OutboundRules` objects

    Attributes returned by API:
        id (str): A UUID to identify and reference a Firewall.
        status (str): A status string indicating the current state of the
            Firewall. This can be "waiting", "succeeded", or "failed".
        created_at (str): The time at which the Firewall was created.
        name (str): The Firewall's name.
        pending_changes (obj:`list`): Details exactly which Droplets are having
            their security policies updated.
        droplet_ids (obj:`list` of `int`): A list of Droplet IDs to be assigned
            to the Firewall.
        tags (obj:`list` of `str`):  A list Tag names to be assigned to the
            Firewall.
        inbound_rules (obj:`list`): A list of `InboundRules` objects
        outbound_rules (obj:`list`): A list of `OutboundRules` objects
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.status = None
        self.created_at = None
        self.pending_changes = []
        self.name = None
        self.inbound_rules = []
        self.outbound_rules = []
        self.droplet_ids = None
        self.tags = None

        super(Firewall, self).__init__(*args, **kwargs)

    @classmethod
    def get_object(cls, api_token, firewall_id):
        """
            Class method that will return a Firewall object by ID.
        """
        firewall = cls(token=api_token, id=firewall_id)
        firewall.load()
        return firewall

    def load(self):
        data = self.get_data("firewalls/%s" % self.id)
        firewall_dict = data['firewall']

        # Setting the attribute values
        for attr in firewall_dict.keys():
            if attr == 'inbound_rules':
                rules = list()
                for rule in firewall_dict['inbound_rules']:
                    rules.append(InboundRule(**rule))
                setattr(self, attr, rules)
            elif attr == 'outbound_rules':
                rules = list()
                for rule in firewall_dict['outbound_rules']:
                    rules.append(OutboundRule(**rule))
                setattr(self, attr, rules)
            else:
                setattr(self, attr, firewall_dict[attr])

        return self

    def add_droplets(self, droplet_ids):
        """
            Add droplets to this Firewall.
        """
        return self.get_data(
            "firewalls/%s/droplets" % self.id,
            type=POST,
            params={"droplet_ids": droplet_ids}
        )

    def remove_droplets(self, droplet_ids):
        """
            Remove droplets from this Firewall.
        """
        return self.get_data(
            "firewalls/%s/droplets" % self.id,
            type=DELETE,
            params={"droplet_ids": droplet_ids}
        )

    def add_tags(self, tags):
        """
            Add tags to this Firewall.
        """
        return self.get_data(
            "firewalls/%s/tags" % self.id,
            type=POST,
            params={"tags": tags}
        )

    def remove_tags(self, tags):
        """
            Remove tags from this Firewall.
        """
        return self.get_data(
            "firewalls/%s/tags" % self.id,
            type=DELETE,
            params={"tags": tags}
        )

    # TODO: Other Firewall calls (Add/Remove rules, Create / Delete etc)

    def destroy(self):
        """
            Destroy the Firewall
        """
        return self.get_data("firewalls/%s/" % self.id, type=DELETE)

    def __str__(self):
        return "<Firewall: %s %s>" % (self.id, self.name)
