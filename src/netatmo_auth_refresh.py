from netatmo_auth_token import read_netatmo_token, refresh_netatmo_token, save_netatmo_token

token_data = read_netatmo_token()
token_data = refresh_netatmo_token(token_data)

save_netatmo_token(token_data)
