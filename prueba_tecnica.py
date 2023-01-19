# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 14:15:24 2023

@author: ADMIN
"""

from hubspot import HubSpot
# import hubspot
from pprint import pprint
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException

def updatePhoneNumber(client, find_key, default_number):
    
    contacts = client.crm.contacts.get_all()
    
    for contact in contacts:
        if not(find_key in contact.properties.keys()):
            contact.properties[find_key] = default_number
            # Intento de actualizar los contacts existentes, falla debido a que
            # properties = { 'email': contact.properties['email'],
            #                'firstname': contact.properties['firstname'],
            #                'lastname': contact.properties['lastname'],
            #                find_key: contact.properties[find_key]
            #              }
            # "phone_number" no existia previamente
            # update_contact = SimplePublicObjectInput(properties=properties)
            # try:
            #     api_response = client.crm.contacts.basic_api.update(contact_id=contact.id, simple_public_object_input=update_contact)
            #     pprint(api_response)
            # except ApiException as e:
            #     print("Exception when calling basic_api->update: %s\n" % e)
    return contacts

def createDealWithContact(client, contacts):
    for contact in contacts:    
        deal_properties = {
            "amount": "1500",
            "closedate": "2019-12-07T16:50:06.678Z",
            "dealname": contact.id + "_" + contact.properties['firstname'],
            "dealstage": "presentationscheduled",
            "pipeline": "default"
            }
        
        deal = SimplePublicObjectInput(properties=deal_properties)
        try:
            deal_response = client.crm.deals.basic_api.create(simple_public_object_input=deal)
            pprint(deal_response)
        except ApiException as e:
            print("Exception when calling basic_api->create: %s\n" % e)
             
            try:
                api_response = client.crm.deals.associations_api.create(deal_id=deal_response.id, to_object_type="contacts", to_object_id=contact.id, association_spec=[{"associationCategory":"HUBSPOT_DEFINED","associationTypeId":3}])
                pprint(api_response)
            except ApiException as e:
                print("Exception when calling associations_api->create: %s\n" % e)

if __name__ == '__main__':
    find_key = 'phone_number'
    default_number = '660049971'

    app_client = HubSpot(access_token='pat-eu1-9492283a-09bc-4833-9dca-8c643d662007')

    contacts = updatePhoneNumber(app_client, find_key, default_number)
    
    createDealWithContact(app_client, contacts)
