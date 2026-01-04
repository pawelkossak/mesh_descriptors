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
        flag = True
        while flag:
            option = input("Options:\n1. Save results to file\n2. Generate and save chart\n3. Exit\nChoose an option (1-3): ")
            match option:
                case "1":
                    print(session.save_descriptors_to_txt())
                case "2":
                    print(session.generate_and_save_chart())
                case "3":
                    print("Exiting...")
                    flag = False


if __name__ == "__main__":
    cliMain()
