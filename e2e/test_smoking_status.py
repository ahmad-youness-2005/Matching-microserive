import requests

class TestSmokingStatus:
    def __init__(self):
        self.base_url = "http://localhost:8000/api/v1"

    def add_smoking_status(self,children_data):
        print(f"Adding a children ...")
        response = requests.post(f"{self.base_url}/smoking-status" , json = children_data )
        if response.status_code >=200 and response.status_code <=299:
            print(f"The user with data {children_data} has been added successfully")
            return response.json()
        else:
            print(f"The data {children_data} with id {children_data['user_id']} failed to be addded")

    def get_smoking_status(self,children_id):
        print(f"Getting the children with ID: {children_id}")
        response = requests.get(f"{self.base_url}/smoking-status/{children_id}")
        response.raise_for_status()
        print(f"The data retrieved for the user with user ID {children_id} is: {response.json()}")
        return response.json()

    def get_all_smoking_status(self):
        print("Getting all smoking status found")
        response = requests.get(f"{self.base_url}/smoking-status")
        if response.status_code >=200 and response.status_code <=299:
            print(f"The data found in the smoking table is {response.json()}")
            return response.json()
        else:
            print("There is no data found in the smoking table")
            return []

    def delete_smoking_status(self , smoking_status_id):
        print(f"Deleting smoking status with ID :{smoking_status_id} ")
        response = requests.delete(f"{self.base_url}/smoking-status/{smoking_status_id}")
        print(f"The data with {smoking_status_id} has been deleted successfully")

    def modify_smoking_status(self , children_id , children_data):
        print(f"Modifying user with ID {children_id}")
        response = requests.put(f"{self.base_url}/smoking-status/{children_id}" , json = children_data)
        if response.status_code >=200 and response.status_code <=299:
            print(f"The modification for user with ID {children_id} have been done successfully")
        else:
            print(f"An error occurred during modifying user with ID: {children_id}")


    def run_smoking_status_operations(self):
        data_for_children = {
            "user_id": "1",
            "does_smoke": True
        }

        modifying_data = {
            "does_smoke":False
        }
        assert len(self.get_all_smoking_status())==0,"There should not be any data "
        children_id = self.add_smoking_status(data_for_children)
        data_id = data_for_children["user_id"]
        returned_data = self.get_smoking_status(data_id)
        assert len(self.get_all_smoking_status())==1,"There should be only one user in the smoking status table"
        assert ( returned_data['does_smoke'] is True),"The does smoke should be true"
        all_smoking_data = self.get_all_smoking_status()
        self.modify_smoking_status(data_id , modifying_data)
        assert (self.get_smoking_status(data_id)['does_smoke'] is False),"The does_smoke attribute should be false"
        deleted_data = self.delete_smoking_status(data_id)
        assert len(self.get_all_smoking_status())==0,"There should not be any data "