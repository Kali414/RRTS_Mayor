from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

Mongo_URL=os.getenv("Mongo_URL")

client=MongoClient(Mongo_URL)

db=client["Practice_1"]

issues=db["Issues"]

issues.insert_many([
    {
        "_id": "I009",
        "location": "Brigade Road",
        "city": "Bengaluru",
        "supervisor_name": "Anita Reddy",
        "repair_status": "In Progress",
        "priority": "High",
        "start_date": "2025-03-05T07:30:00.000+00:00",
        "completion_date": "2025-03-20T09:30:00.000+00:00",
        "estimated_cost": 25000,
        "repair_type": "Bridge Repair",
        "materials_used": ["Steel", "Concrete"],
        "comments": "Structural reinforcement ongoing",
        "images": [
            "https://example.com/repair13.jpg",
            "https://example.com/repair14.jpg"
        ]
    },
    {
        "_id": "I010",
        "location": "Marine Drive",
        "city": "Mumbai",
        "supervisor_name": "Rajesh Mehta",
        "repair_status": "Completed",
        "priority": "Medium",
        "start_date": "2025-02-10T10:00:00.000+00:00",
        "completion_date": "2025-02-18T16:00:00.000+00:00",
        "estimated_cost": 40000,
        "repair_type": "Sea Wall Reinforcement",
        "materials_used": ["Concrete", "Steel Rods"],
        "comments": "Reinforced to prevent coastal erosion",
        "images": [
            "https://example.com/repair15.jpg",
            "https://example.com/repair16.jpg"
        ]
    },
    {
        "_id": "I011",
        "location": "Salt Lake Sector 5",
        "city": "Kolkata",
        "supervisor_name": "Piyush Saha",
        "repair_status": "Pending",
        "priority": "Low",
        "start_date": "2025-03-15T12:30:00.000+00:00",
        "completion_date": "2025-03-20T09:30:00.000+00:00",
        "estimated_cost": 12000,
        "repair_type": "Streetlight Fix",
        "materials_used": ["LED Bulbs", "Electric Cables"],
        "comments": "Approval pending from electrical board",
        "images": [
            "https://example.com/repair17.jpg",
            "https://example.com/repair18.jpg"
        ]
    },
    {
        "_id": "I012",
        "location": "Banjara Hills",
        "city": "Hyderabad",
        "supervisor_name": "Suresh Kumar",
        "repair_status": "In Progress",
        "priority": "High",
        "start_date": "2025-03-03T08:45:00.000+00:00",
        "completion_date": "2025-03-20T09:30:00.000+00:00",
        "estimated_cost": 35000,
        "repair_type": "Road Resurfacing",
        "materials_used": ["Asphalt", "Gravel"],
        "comments": "Heavy traffic, work only at night",
        "images": [
            "https://example.com/repair19.jpg",
            "https://example.com/repair20.jpg"
        ]
    },
    {
        "_id": "I013",
        "location": "Sector 62",
        "city": "Noida",
        "supervisor_name": "Vikram Singh",
        "repair_status": "Completed",
        "priority": "Medium",
        "start_date": "2025-02-28T09:00:00.000+00:00",
        "completion_date": "2025-03-05T18:30:00.000+00:00",
        "estimated_cost": 22000,
        "repair_type": "Pothole Fix",
        "materials_used": ["Bitumen", "Tar"],
        "comments": "Completed successfully, minor touch-ups left",
        "images": [
            "https://example.com/repair21.jpg",
            "https://example.com/repair22.jpg"
        ]
    },
    {
        "_id": "I014",
        "location": "Gomti Nagar",
        "city": "Lucknow",
        "supervisor_name": "Arun Tiwari",
        "repair_status": "Pending",
        "priority": "Low",
        "start_date": "2025-03-18T10:15:00.000+00:00",
        "completion_date": "2025-03-20T09:30:00.000+00:00",
        "estimated_cost": 18000,
        "repair_type": "Drainage Fix",
        "materials_used": ["PVC Pipes", "Cement"],
        "comments": "Survey completed, work to begin soon",
        "images": [
            "https://example.com/repair23.jpg",
            "https://example.com/repair24.jpg"
        ]
    },
    {
        "_id": "I015",
        "location": "Law Garden",
        "city": "Ahmedabad",
        "supervisor_name": "Ramesh Patel",
        "repair_status": "In Progress",
        "priority": "High",
        "start_date": "2025-03-07T11:00:00.000+00:00",
        "completion_date": "2025-03-20T09:30:00.000+00:00",
        "estimated_cost": 27000,
        "repair_type": "Sidewalk Repair",
        "materials_used": ["Concrete", "Paver Blocks"],
        "comments": "Work in progress, pedestrian safety ensured",
        "images": [
            "https://example.com/repair25.jpg",
            "https://example.com/repair26.jpg"
        ]
    },
    {
        "_id": "I016",
        "location": "Rajpath",
        "city": "New Delhi",
        "supervisor_name": "Neha Sharma",
        "repair_status": "Completed",
        "priority": "High",
        "start_date": "2025-02-05T07:45:00.000+00:00",
        "completion_date": "2025-02-12T13:15:00.000+00:00",
        "estimated_cost": 50000,
        "repair_type": "Road Resurfacing",
        "materials_used": ["Asphalt", "Concrete Mix"],
        "comments": "Completed before Republic Day celebrations",
        "images": [
            "https://example.com/repair27.jpg",
            "https://example.com/repair28.jpg"
        ]
    },
    {
        "_id": "I017",
        "location": "Mall Road",
        "city": "Shimla",
        "supervisor_name": "Prakash Rana",
        "repair_status": "Pending",
        "priority": "Medium",
        "start_date": "2025-03-20T09:30:00.000+00:00",
        "completion_date": "2025-03-20T09:30:00.000+00:00",
        "estimated_cost": 16000,
        "repair_type": "Streetlight Fix",
        "materials_used": ["LED Lamps", "Metal Poles"],
        "comments": "Snowfall may delay work",
        "images": [
            "https://example.com/repair29.jpg",
            "https://example.com/repair30.jpg"
        ]
    }
]

)