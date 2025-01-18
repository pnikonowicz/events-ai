import os
from eventbrite import Eventbrite

def get_eventbrite_data(token):
    eventbrite = Eventbrite(token)
    user = eventbrite.get_user()  # Not passing an argument returns yourself
    print("id: " + user['id'])

def load_oauth_token(current_dir):
    token_path = "secrets/oauth.token"
    file_path = os.path.join(current_dir, token_path)

    with open(file_path, "r") as file:
        return file.read().strip()        
    

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    token = load_oauth_token(current_dir)
    # print("token: " + token)
    get_eventbrite_data(token)