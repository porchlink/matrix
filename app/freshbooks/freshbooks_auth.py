import json
import webbrowser

from types import SimpleNamespace
from freshbooks import Client as FreshBooksClient

def auth():
    with open('./app/freshbooks/fb_.json') as f:
        data = json.load(f)

    freshBooksClient = FreshBooksClient(
        client_id=data[0]['FB_CLIENT_ID'],
        client_secret=data[0]['SECRET'],
        redirect_uri=data[0]['REDIRECT_URI'], 
    )

    try:
        token_response = freshBooksClient.refresh_access_token(data[0]['refresh_token']) 
    except Exception as e:
        print(e)
        authorization_url = freshBooksClient.get_auth_request_url(
            scopes=['user:profile:read', 'user:clients:read', 'user:invoices:read']
        )
        webbrowser.get().open(authorization_url)

        auth_code = input("Enter the code you get after authorization: ")
        token_response = freshBooksClient.get_access_token(auth_code)

    data[0]['refresh_token'] = token_response.refresh_token
    with open('./app/freshbooks/fb_.json', 'w') as f:
        json.dump(data, f)

    # Get the current user's identity
    identity = freshBooksClient.current_user()
    businesses = []

    # Display all of the businesses the user has access to
    # for num, business_membership in enumerate(identity.business_memberships, start=1):
    #     business = business_membership.business
    #     businesses.append(
    #         SimpleNamespace(name=business.name, business_id=business.id, account_id=business.account_id)
    #     )
    #     print(f"{num}: {business.name}")
    # business_index = 0#int(input("Which business do you want to use? ")) - 1
    # print()
    # business_id = businesses[business_index].business_id  # Used for project-related calls
    # account_id = businesses[business_index].account_id  # Used for accounting-related calls

    acc_id = identity.data['business_memberships'][0]['business']['account_id']
    #client = freshBooksClient.clients.list(acc_id)[0]
    #print(f"'{client.organization}' is a client of {businesses[business_index].name}")
    return freshBooksClient, acc_id

