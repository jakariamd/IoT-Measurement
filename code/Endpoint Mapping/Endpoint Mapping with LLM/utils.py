import openai

OPENAI_API_KEY = 'sk-YOUR-OPENAI-KEY'
openai.api_key = OPENAI_API_KEY


def chat_completion(messages):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=64,
        temperature=0.2)


def map_org_domain(org, domain):
    messages = [
        {"role": "system", "content": "You are an expert in finding the relationship between a company and a domain."
                                      "You will be given a company name and a domain link. "
                                      "You will search for the domain owner and match it with the company name."
                                      "If it match, say the domain is first party to the company."
                                      "Or if it does not match, search what type of service the domain provides."
                                      "If the service type is CDN, cloud platform, IoT backend provide, or any other business relationship with the company,"
                                      " mark it as a support party. Otherwise mark the domain as a third party."},
        {"role": "user", "content": "Now, given company name is '" + org +
                                    "' and the domain name is '" + domain +
                                    "' classify as 'first party' or 'support party' or 'third party'."
                                    "  output only classification word and explanation within 50 words "}
        ]

    completion = chat_completion(messages)
    explanation = completion.choices[0].message.content

    return explanation

# Test map_org_domain
# map_org_domain("Google", "docker.com")
