import requests
from typing import Optional, Dict, List


class APIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user: Optional[Dict] = None
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    
    def register(self, username: str, email: str, password: str, 
                 first_name: str = "", last_name: str = "") -> Dict:
        """Register a new user"""
        url = f"{self.base_url}/auth/register/"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        self.access_token = result.get("access")
        self.refresh_token = result.get("refresh")
        self.user = result.get("user")
        
        return result
    
    def login(self, username: str, password: str) -> Dict:
        """Login user"""
        url = f"{self.base_url}/auth/login/"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        
        self.access_token = result.get("access")
        self.refresh_token = result.get("refresh")
        self.user = result.get("user")
        
        return result
    
    def get_profile(self) -> Dict:
        """Get user profile"""
        url = f"{self.base_url}/auth/profile/"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def upload_csv(self, file_path: str) -> Dict:
        """Upload CSV file"""
        url = f"{self.base_url}/datasets/upload/"
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, headers=headers)
        
        response.raise_for_status()
        return response.json()
    
    def get_datasets(self) -> List[Dict]:
        """Get all datasets"""
        url = f"{self.base_url}/datasets/"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_dataset_detail(self, dataset_id: int) -> Dict:
        """Get dataset details"""
        url = f"{self.base_url}/datasets/{dataset_id}/"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def delete_dataset(self, dataset_id: int) -> Dict:
        """Delete dataset"""
        url = f"{self.base_url}/datasets/{dataset_id}/delete/"
        response = requests.delete(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def download_report(self, dataset_id: int, save_path: str):
        """Download PDF report"""
        url = f"{self.base_url}/datasets/{dataset_id}/report/"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.access_token is not None
