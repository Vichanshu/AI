import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")

text ="Hey this is Vichanshu , how are you Shreya?"

token = enc.encode(text)

print("token: ",token)

decoded = enc.decode(token)

print ("decoded: ", decoded)

