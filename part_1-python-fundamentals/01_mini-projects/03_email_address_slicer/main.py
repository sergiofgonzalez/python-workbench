email = input("Please type your email address: ")
print("Your email address is: ", email)

email_parts = email.split("@")
if len(email_parts) != 2:
    print(f"Incorrect input: a valid email was expected but got '{email}'")
    raise SystemExit

email_username = email_parts[0]
email_domain = email_parts[1]

email_domain_parts = email_domain.split(".")
if len(email_domain_parts) < 2:
    print("Incorrect input: a valid email(a@b.c)" +
          f"was expected but got '{email}'")
    raise SystemExit

email_domain_ext = email_domain_parts[-1]
email_domain_name = email_domain[:-len(email_domain_ext)-1]

print("username              :", email_username)
print("email domain          :", email_domain)
print("email domain name     :", email_domain_name)
print("email domain extension:", email_domain_ext)
