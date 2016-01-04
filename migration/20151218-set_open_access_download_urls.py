#!/usr/bin/env python
"""Look up and set the open access download url for all books."""
from nose.tools import set_trace
import os
import sys
bin_dir = os.path.split(__file__)[0]
package_dir = os.path.join(bin_dir, "..")
sys.path.append(os.path.abspath(package_dir))
from core.monitor import IdentifierSweepMonitor
from core.model import (
    Identifier,
    Representation,
    DeliveryMechanism,
)
from core.opds_import import SimplifiedOPDSLookup
from core.scripts import RunMonitorScript

class SetDeliveryMechanismMonitor(IdentifierSweepMonitor):

    def __init__(self, _db, interval_seconds=None):
        super(SetDeliveryMechanismMonitor, self).__init__(
            _db, "20151218 migration - Set open access download urls", 
            interval_seconds, batch_size=10)

    def process_identifier(self, identifier):
        license_pool = identifier.licensed_through
        if not license_pool:
            print "No license pool for %s!" % identifier.identifier
            return
        edition = license_pool.edition
        if edition:
            best = edition.best_open_access_link
            if best:
                print edition.id, edition.title, best.url
                edition.set_open_access_link()
            else:
                print "Edition but no link for %s/%s!" % (
                    identifier.identifier, edition.title)
        else:
            print "No edition for %s!" % identifier.identifier

RunMonitorScript(SetDeliveryMechanismMonitor).run()
