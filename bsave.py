import os

class PersistentStorage():
    """
    A class to save and retrieve a dictionary to disk without using pickle, json, or binary writing.
    It relies on simple text file storage.
    """

    def __init__(self, filename):
        """
        Initializes the PersistentDictionary with a filename.

        Args:
            filename: The name of the file to store the dictionary in.
        """
        self.filename = filename

    def save(self, dictionary):
        """
        Appends a dictionary to a list of dictionaries stored in a file.
        Avoids using pickle or JSON.

        Args:
            self.filename: The path to the file.
            dictionary: The dictionary to append.  It's important that the dictionary's
                         values can be represented as strings.
        """

        try:
            # Try to open the file in append mode ('a')
            with open(self.filename, 'a') as f:
                # Convert the dictionary to a string representation
                dict_str = str(dictionary)  # This is crucial; values must be stringable.
                f.write(dict_str + '\n')  # Add a newline to separate dictionaries

            #print(f"Dictionary appended to {self.filename}")

        except Exception as e:
            print(f"Error appending dictionary to file: {e}")


    def load(self):
        """
        Retrieves a list of dictionaries from a file.
        Avoids using pickle or JSON.

        Args:
            self.filename: The path to the file.

        Returns:
            A list of dictionaries, or an empty list if the file doesn't exist or is empty.
        """

        try:
            if not os.path.exists(self.filename):
                print(f"File {self.filename} does not exist.")
                return []

            dictionaries = []
            with open(self.filename, 'r') as f:
                for line in f:
                    line = line.strip()  # Remove leading/trailing whitespace
                    if line: # Skip empty lines
                        try:
                            dictionary = eval(line)  # Use eval (with caution - see notes below)
                            if isinstance(dictionary, dict):
                                if (not dictionary["model"]):
                                    raise ValueError("Not compatible file.")
                                elif (not dictionary["role"]):
                                    raise ValueError("Not compatible file.")
                                elif (not dictionary["content"]):
                                    raise ValueError("Not compatible file.")
                                elif (not dictionary["session_id"]):
                                    raise ValueError("Not compatible file.")
                                elif (not dictionary["conversation_id"]):
                                    raise ValueError("Not compatible file.")
                                elif (dictionary["model"] and dictionary ["role"] and dictionary ["content"] and dictionary ["session_id"] and dictionary ["conversation_id"]):
                                    dictionaries.append(dictionary)
                                    
                            else:
                                print(f"Warning: Line '{line}' does not represent a dictionary. Skipping.")

                        except (SyntaxError, NameError) as e:
                            print(f"Error parsing line '{line}': {e}.  Skipping.")
            return dictionaries

        except Exception as e:
            print(f"Error retrieving dictionaries from file: {e}")
            return []

