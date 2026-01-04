from classes import MeshSession

def cliMain():
    search_text = input("Enter medical text to search for MeSH descriptors: ")
    session = MeshSession(search_text)
    descriptors = session.get_descriptors()
    if len(descriptors) == 0:
        print("No descriptors found")
    else:
        count = len(descriptors)
        plural = "" if count == 1 else "s"
        print(f"Found {count} most common descriptor{plural}:")
        for descriptor, count in descriptors:
            print(f"{descriptor}: {count}")
        


if __name__ == "__main__":
    cliMain()