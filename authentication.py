import os.path
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

def get_contacts():
    """Lấy danh sách liên hệ từ Google Contacts"""
    try:
        # Xác thực
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        # Kết nối API
        service = build('people', 'v1', credentials=creds)
        
        # Lấy nhóm liên hệ
        groups_dict = _get_contact_groups(service)
        
        # Lấy danh bạ
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=100,
            personFields='names,emailAddresses,organizations,memberships'
        ).execute()

        connections = results.get('connections', [])
        contacts_data = []
        
        for person in connections:
            names = person.get('names', [])
            emails_data = person.get('emailAddresses', [])
            
            if names and emails_data:
                name = names[0].get('displayName')
                email = emails_data[0].get('value')
                
                # Chức danh và công ty
                title = ''
                organizations = person.get('organizations', [])
                if organizations:
                    org = organizations[0]
                    title = org.get('title', '')
                
                # Nhãn/nhóm
                labels = []
                memberships = person.get('memberships', [])
                for membership in memberships:
                    contact_group = membership.get('contactGroupMembership', {})
                    if contact_group:
                        group_id = contact_group.get('contactGroupResourceName', '').replace('contactGroups/', '')
                        if group_id:
                            # Mapping system labels
                            system_labels = {
                                'myContacts': 'Liên hệ của tôi',
                                'starred': 'Quan trọng',
                                'blocked': 'Bị chặn',
                                'family': 'Gia đình',
                                'friends': 'Bạn bè',
                                'coworkers': 'Đồng nghiệp'
                            }
                            
                            label_name = system_labels.get(group_id, groups_dict.get(group_id, 'Nhóm tùy chỉnh'))
                            labels.append(label_name)
                
                contacts_data.append({
                    'name': name,
                    'email': email,
                    'title': title,
                    'labels': labels
                })

        return contacts_data

    except FileNotFoundError:
        print("❌ Không tìm thấy credentials.json!")
        return []
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return []

def _get_contact_groups(service):
    """Lấy danh sách tên nhóm/nhãn từ ID"""
    try:
        groups_result = service.contactGroups().list().execute()
        contact_groups = groups_result.get('contactGroups', [])
        
        groups_dict = {}
        for group in contact_groups:
            group_resource_name = group.get('resourceName', '')
            group_id = group_resource_name.replace('contactGroups/', '')
            
            try:
                group_detail = service.contactGroups().get(
                    resourceName=group_resource_name,
                    maxMembers=0
                ).execute()
                
                group_name = group_detail.get('name', '')
                formatted_name = group_detail.get('formattedName', '')
                final_name = formatted_name or group_name or group_id
                
                if final_name:
                    groups_dict[group_id] = final_name
                    
            except:
                group_name = group.get('name', group_id)
                groups_dict[group_id] = group_name
        
        return groups_dict
        
    except Exception:
        return {}

def test_contacts():
    """Test function để kiểm tra"""
    print("🧪 Testing Google Contacts...")
    contacts = get_contacts()
    
    if contacts:
        print(f"✅ Lấy được {len(contacts)} liên hệ")
        
        # Backup
        with open('contacts_backup.json', 'w', encoding='utf-8') as f:
            json.dump(contacts, f, ensure_ascii=False, indent=2)
        
        # Thống kê
        has_title = sum(1 for c in contacts if c.get('title'))
        has_labels = sum(1 for c in contacts if c.get('labels'))
        
        print(f"📊 Có chức danh: {has_title}, Có nhãn: {has_labels}")
        
        # Hiển thị vài ví dụ
        for i, contact in enumerate(contacts[:3], 1):
            display = f"{i}. {contact['name']}: {contact['email']}"
            if contact.get('title'):
                display += f" ({contact['title']})"
            if contact.get('company'):
                display += f" tại {contact['company']}"
            if contact.get('labels'):
                display += f" [Nhãn: {', '.join(contact['labels'])}]"
            print(display)
            
    else:
        print("❌ Test thất bại!")

if __name__ == "__main__":
    test_contacts()
