import library_pb2  

def read_protobuf(file_path):
    message = library_pb2.Books()

    with open(file_path, "rb") as f:
        message.ParseFromString(f.read())

    return message

protobuf_data = read_protobuf('books')

print(protobuf_data)