"""
ContractShipping Canada Post API
https://www.canadapost.ca/cpo/mc/business/productsservices/developers/services/shippingmanifest/default.jsf
"""
import logging
from lxml import etree
import requests
from canada_post.service import ServiceBase
from canada_post.util import InfoObject

class Shipment(InfoObject):
    """
    """
class CreateShipment(ServiceBase):
    """
    CreateShipment Canada Post API (for ContractShipping)
    https://www.canadapost.ca/cpo/mc/business/productsservices/developers/services/shippingmanifest/createshipment.jsf
    """
    URL ="https://{server}/rs/{customer}/{mobo}/shipment"
    log = logging.getLogger('canada_post.service.contract_shipping'
                            '.CreateShipment')
    def __init__(self, auth, url=None):
        if url:
            self.URL = url
        super(CreateShipment, self).__init__(auth)

    def set_link(self, url):
        """
        Sets the link in case you want to set it after initialization
        """
        self.URL = url

    def get_url(self):
        return self.URL.format(server=self.get_sever(),
                               customer=self.auth.customer_number,
                               mobo=self.auth.customer_number)

    def _create_address_detail(self, parent, address, add_child):
        """
        Creates the address detail part of the request. You need to do any
        checks outside of this call
        """
        addr_detail = add_child("address-details", parent)
        add_child("address-line-1", addr_detail).text = address.address1
        add_child("address-line-2", addr_detail).text = address.address2
        add_child("city", addr_detail).text = address.city
        if address.province:
            add_child("prov-state", addr_detail).text = address.province
        add_child("country-code", addr_detail).text = address.country_code
        if address.postal_code:
            add_child("postal-zip-code",
                      addr_detail).text = unicode(address.postal_code)
        else:
            assert address.country_code not in ("US", "CA"), (
                "Addresses within {} require "
                "a postal code").format(address.country_code)

        return addr_detail

    def __call__(self, parcel, origin, destination, service, group):
        """
        Create a shipping order for the given parcels

        parcel: must be a canada_post.util.parcel.Parcel
        origin: must be a canada_post.util.address.Origin instance
        destination: must be a canada_post.util.address.Destination instance
        service: must be a canada_post.service.Service instance with at least
            the code parameter set up
        group: must be a string or unicode defining the parcel group that this
            parcel should be added to
        """
        debug = "( DEBUG )" if self.auth.debug else ""
        self.log.info(("Create shipping for parcel %s, from %s to %s{debug}"
                       .format(debug=debug)), parcel, origin, destination)

        # shipment
        shipment = etree.Element(
            "shipment", xmlns="http://www.canadapost.ca/ws/shipment")
        def add_child(child_name, parent=shipment):
            return etree.SubElement(parent, child_name)
        add_child("group-id").text = group
        add_child("requested-shipping-point").text = unicode(origin.postal_code)
        delivery_spec = add_child("delivery-spec")
        add_child("service-code", delivery_spec).text = service.code

        # sender
        sender = add_child("sender", delivery_spec)
        if origin.name:
            add_child("name", sender).text = origin.name
        assert origin.company, ("The sender needs a company name for "
                                "Contract Shipping service")
        add_child("company", sender).text = origin.company
        assert origin.phone, ("The sender needs a phone for "
                              "Contact Shipping Service")
        add_child("contact-phone", sender).text = origin.phone

        #destination details, first assertions
        assert any((origin.address1, origin.address2)), (
            "The sender needs an address to Create Shipping")
        assert origin.city, "Need the sender's city to Create Shipping"
        assert origin.province, "Need the sender's province to Create Shipping"
        sender_details = self._create_address_detail(sender, origin, add_child)
        # done sender

        # destination
        dest = add_child("destination", delivery_spec)
        if destination.name:
            add_child("name", dest).text = destination.name
        else:
            # TODO: if the Deliver to Post Office option is used, the name
            #  element must be present for the destination.
            pass
        if destination.company:
            add_child("company", dest).text = destination.company
        if destination.extra:
            add_child("additional-address-info").text = destination.extra
        if destination.phone:
            add_child("client-voice-number", dest).text = destination.phone
        else:
            # Required for destination when service is one of
            #  Expedited Parcel-USA, Xpresspost-USA, Xpresspost-International,
            #  Priority Worldwide Parcel or Pak
            #  (USA.EP, USA.XP, INT.XP, USA.PW.PARCEL, USA.PW.PAK,
            #   INT.PW.PARCEL, INT.PW.PAK)
            if service.code in ("USA.EP", "USA.XP", "INT.XP", "USA.PW.PARCEL",
                                "USA.PW.PAK", "INT.PW.PARCEL", "INT.PK.PAK"):
                assert False, ("Service {code} requires destination to have a "
                               "phone number").format(code=service.code)

        # destination details, first assertions
        assert any((destination.address1, destination.address2)), (
            "Must have address to Create Shipping")
        if not destination.province:
            assert destination.country_code not in ("CA", "US"), (
                "Country code is required for international shippings")
        # and then creation
        dest_details = self._create_address_detail(dest, destination, add_child)
        # done destination

        # TODO: options
        #options = add_child("options", delivery_spec)

        # parcel
        parcel_chars = add_child("parcel-characteristics", delivery_spec)
        add_child("weight", parcel_chars).text = unicode(parcel.weight)
        if all((parcel.length > 0, parcel.width > 0, parcel.height > 0)):
            dims = add_child("dimensions", parcel_chars)
            add_child("length", dims).text = unicode(parcel.length)
            add_child("width", dims).text = unicode(parcel.width)
            add_child("height", dims).text = unicode(parcel.height)
        add_child("unpackaged", parcel_chars).text = ("true"
                                                      if parcel.unpackaged
                                                      else "false")

        # TODO: notification
        #notification = add_child("notification", delivery_spec)

        # TODO: print-preferences
        #print_preferences = add_child("print-preferences", delivery_spec)

        # preferences
        preferences = add_child("preferences", delivery_spec)
        add_child("show-packing-instructions", preferences).text = "false"
        # TODO: these two are actually optional (may be "false") for CA
        # shippings
        add_child("show-postage-rate", preferences).text = "false"
        add_child("show-insured-value", preferences).text = "false"

        # settlement-info
        settlement = add_child("settlement-info", delivery_spec)
        # TODO: set paid-by-customer if a different customer is paying for this
        #add_child("paid-by-customer", settlement).text = FOOBAR
        assert self.auth.contract_number, ("Must have a contract number for "
                                           "contract shipping")
        add_child("contract-id", settlement).text = self.auth.contract_number
        # TODO: can be CreditCard as well
        add_child("intended-method-of-payment", settlement).text = "Account"

        headers = {
            'Accept': "application/vnd.cpc.shipment-v2+xml",
            'Content-type': "application/vnd.cpc.shipment-v2+xml",
            'Accept-language': "en-CA",
        }
        url = self.get_url()
        request = etree.tostring(shipment, pretty_print=True)
        return request, url, headers
        requests.post(url=url, data=request, headers=headers,
                      auth=self.userpass())
