#!/usr/bin/env python
import os
import sys
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trek_expenses.settings')
django.setup()

# Now you can import your models
from clients.models import Client, PriceItem

def generate_test_data():
    print("Generating realistic client data...")
    
    # Real names for clients
    real_names = [
        "John Anderson", "Sarah Mitchell", "Michael Chen", "Emma Wilson", 
        "David Rodriguez", "Julia Schmidt", "Thomas Brown", "Sophia Lee",
        "James Taylor", "Maria Garcia", "Robert Johnson", "Laura Martinez", 
        "Daniel Kim", "Olivia Williams", "William Davis", "Isabella Lopez",
        "Richard Thompson", "Emily White", "Alexander Clark", "Sofia Nguyen",
        "Christopher Baker", "Ava Patel", "Matthew Lewis", "Charlotte Moore",
        "Joseph Walker", "Amelia Scott", "Andrew Hill", "Elizabeth Green",
        "Ryan Adams", "Grace Turner", "Joshua Phillips", "Lily Campbell",
        "Kevin Evans", "Hannah King", "Brian Parker", "Victoria Wright",
        "Jacob Stewart", "Natalie Allen", "Jonathan Young", "Chloe Hall",
        "Tyler Morris", "Zoe Carter", "Brandon Rogers", "Audrey Gray",
        "Jason Powell", "Sophie Hughes", "Adam Morgan", "Maya Foster"
    ]
    
    # Create a list of realistic trek packages with detailed descriptions
    trek_packages = [
        {"name": "Everest Base Camp Trek", "duration": 14, "elevation": "5,364m", "difficulty": "Moderate to Difficult"},
        {"name": "Annapurna Circuit", "duration": 16, "elevation": "5,416m", "difficulty": "Moderate to Difficult"},
        {"name": "Manaslu Circuit", "duration": 15, "elevation": "5,160m", "difficulty": "Difficult"},
        {"name": "Langtang Valley Trek", "duration": 10, "elevation": "3,870m", "difficulty": "Moderate"},
        {"name": "Upper Mustang Trek", "duration": 14, "elevation": "3,810m", "difficulty": "Moderate"},
        {"name": "Kanchenjunga Base Camp", "duration": 18, "elevation": "5,140m", "difficulty": "Difficult"},
        {"name": "Gokyo Lakes Trek", "duration": 12, "elevation": "5,357m", "difficulty": "Moderate to Difficult"},
        {"name": "Mera Peak Climbing", "duration": 16, "elevation": "6,476m", "difficulty": "Very Difficult"},
        {"name": "Island Peak Climbing", "duration": 15, "elevation": "6,189m", "difficulty": "Very Difficult"},
        {"name": "Annapurna Base Camp", "duration": 11, "elevation": "4,130m", "difficulty": "Moderate"},
        {"name": "Three Passes Trek", "duration": 18, "elevation": "5,535m", "difficulty": "Difficult"},
        {"name": "Ghorepani Poon Hill Trek", "duration": 7, "elevation": "3,210m", "difficulty": "Easy to Moderate"},
        {"name": "Helambu Circuit", "duration": 9, "elevation": "3,640m", "difficulty": "Moderate"},
        {"name": "Dhaulagiri Circuit", "duration": 17, "elevation": "5,360m", "difficulty": "Difficult"},
        {"name": "Rara Lake Trek", "duration": 10, "elevation": "2,990m", "difficulty": "Moderate"}
    ]
    
    # List of experienced guides with real names and experience levels
    guides = [
        {"name": "Pasang Sherpa", "experience": "20+ years", "specialty": "High Altitude Climbing"},
        {"name": "Mingma Dorjee", "experience": "15 years", "specialty": "Everest Region"},
        {"name": "Tenzin Norbu", "experience": "18 years", "specialty": "Technical Climbing"},
        {"name": "Pemba Rinzin", "experience": "12 years", "specialty": "Annapurna Region"},
        {"name": "Dawa Tamang", "experience": "22 years", "specialty": "Remote Treks"},
        {"name": "Karma Gurung", "experience": "16 years", "specialty": "Cultural Tours"},
        {"name": "Nima Dorjee", "experience": "14 years", "specialty": "Manaslu Region"},
        {"name": "Lakpa Tenzing", "experience": "19 years", "specialty": "Photography Treks"},
        {"name": "Ang Tshering", "experience": "25 years", "specialty": "Expedition Leadership"},
        {"name": "Kaji Tamang", "experience": "17 years", "specialty": "Langtang Region"},
        {"name": "Sonam Sherpa", "experience": "15 years", "specialty": "Peak Climbing"},
        {"name": "Gyalzen Bhutia", "experience": "13 years", "specialty": "Nature Tours"}
    ]
    
    # List of countries
    countries = [
        "USA", "UK", "Germany", "France", "Australia", "Canada", "Japan",
        "South Korea", "Netherlands", "Italy", "Spain", "Switzerland", 
        "Sweden", "Norway", "Denmark", "Belgium", "India", "Israel"
    ]
    
    # Create clients one by one with error handling
    created_clients = []
    
    # Shuffle the names to ensure random distribution
    random.shuffle(real_names)
    
    for i, name in enumerate(real_names, 1):
        try:
            # Select a random trek
            trek = random.choice(trek_packages)
            # Adjust trek duration by +/- 2 days for variability
            trek_duration = trek["duration"] + random.randint(-2, 2)
            trek_duration = max(5, trek_duration)  # Ensure minimum 5 days
            
            # Select a guide appropriate for this trek
            guide = random.choice(guides)
            
            # Generate random dates in 2025
            start_month = random.randint(3, 11)  # March to November (trekking season)
            start_day = random.randint(1, 28)
            
            # Create a distribution where more treks are in peak seasons
            if random.random() < 0.7:  # 70% chance for peak season
                start_month = random.choice([3, 4, 5, 9, 10, 11])
            
            starting_date = datetime(2025, start_month, start_day).date()
            
            # Calculate ending date
            ending_date = starting_date + timedelta(days=trek_duration - 1)
            
            # Determine trek type based on package name
            is_trekking = "Peak" not in trek["name"]
            is_peak_climbing = "Peak" in trek["name"]
            is_tour = random.random() < 0.1  # 10% chance of being a tour as well
            is_adventure = random.random() < 0.15  # 15% chance of including adventure activities
            is_flight = random.random() < 0.6  # 60% chance of including a flight
            
            # Random porter arrangement
            porter_count = random.randint(1, 3) if (is_trekking or is_peak_climbing) else 0
            porter_text = f"{porter_count} Porters" if porter_count > 0 else ""
            
            # Random pricing based on trek type and duration
            base_price = None
            if is_peak_climbing:
                base_price = Decimal(str(2000 + (trek_duration * 150) + random.randint(0, 300)))
            elif is_trekking:
                base_price = Decimal(str(1200 + (trek_duration * 80) + random.randint(0, 300)))
            elif is_tour:
                base_price = Decimal(str(800 + (trek_duration * 100) + random.randint(0, 200)))
            else:
                base_price = Decimal(str(500 + (trek_duration * 70) + random.randint(0, 200)))
            
            # Trekking days is typically a bit less than total days
            trekking_days = trek_duration - random.randint(1, 3) if (is_trekking or is_peak_climbing) else None
            
            # Payment status with realistic distribution
            payment_status_choices = ['pending', 'partial', 'completed']
            payment_weights = [0.15, 0.25, 0.6]  # 15% pending, 25% partial, 60% completed
            payment_status = random.choices(payment_status_choices, weights=payment_weights, k=1)[0]
            
            # Generate a coherent email from the name
            first_name, last_name = name.split(' ', 1)
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"
            
            # Create passport number with country code
            country = random.choice(countries)
            country_code = country[0]
            passport = f"{country_code}{random.randint(10000000, 99999999)}"
            
            # Create client
            client = Client(
                client_name=name,
                email=email,
                country=country,
                passport=passport,
                phone_number=f"+{random.randint(1, 99)}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                quick_notes=f"Interested in {trek['name']}. Difficulty: {trek['difficulty']}. Max elevation: {trek['elevation']}." if random.random() < 0.7 else "",
                starting_date=starting_date,
                ending_date=ending_date,
                total_days=trek_duration,
                trekking=is_trekking,
                peak_climbing=is_peak_climbing,
                tour=is_tour,
                adventure_day_activities=is_adventure,
                flight=is_flight,
                misc_service="" if random.random() < 0.8 else random.choice(["Photography Tour", "Cultural Experience", "Meditation Retreat"]),
                guide=guide["name"],
                porter=porter_text,
                package=trek["name"],
                transport=random.choice(["Private Jeep", "Tourist Bus", "Domestic Flight", "Private Car", ""]),
                accommodation=random.choice(["Tea Houses", "Hotels", "Camping", "Mixed", "Local Homestay"]),
                price=base_price,
                additional_charges=Decimal(str(random.randint(0, 500))) if random.random() < 0.4 else Decimal('0'),
                discount=Decimal(str(random.randint(0, 300))) if random.random() < 0.3 else Decimal('0'),
                payment_status=payment_status,
                notification_sent=random.random() < 0.2
            )
            
            # Set trekking_days separately if it has a value
            if trekking_days is not None:
                client.trekking_days = trekking_days
                
            # Save the client
            client.save()
            created_clients.append(client)
            print(f"Created client: {client.client_name} - {trek['name']}")
            
            # Create 1-3 price items for this client
            num_items = random.randint(1, 3)
            for j in range(num_items):
                # More realistic price items based on trek type
                item_choices = []
                
                if is_peak_climbing:
                    item_choices = [
                        {"description": "Climbing Equipment Rental", "amount": Decimal(str(180 + random.randint(20, 150)))},
                        {"description": "Climbing Permit Fee", "amount": Decimal(str(250 + random.randint(30, 100)))},
                        {"description": "High Altitude Insurance", "amount": Decimal(str(200 + random.randint(50, 150)))},
                        {"description": "Technical Guide Fee", "amount": Decimal(str(300 + random.randint(50, 150)))},
                        {"description": "Oxygen Cylinder", "amount": Decimal(str(150 + random.randint(20, 100)))}
                    ]
                elif is_trekking:
                    item_choices = [
                        {"description": "Trekking Equipment Rental", "amount": Decimal(str(80 + random.randint(20, 120)))},
                        {"description": "Trekking Permit", "amount": Decimal(str(120 + random.randint(30, 80)))},
                        {"description": "Travel Insurance", "amount": Decimal(str(150 + random.randint(50, 100)))},
                        {"description": "Porter Equipment", "amount": Decimal(str(60 + random.randint(10, 40)))},
                        {"description": "Special Meals Package", "amount": Decimal(str(70 + random.randint(30, 50)))}
                    ]
                else:
                    item_choices = [
                        {"description": "Airport Transfer", "amount": Decimal(str(50 + random.randint(10, 30)))},
                        {"description": "Cultural Tour Guide", "amount": Decimal(str(100 + random.randint(30, 70)))},
                        {"description": "Museum Entrance Fees", "amount": Decimal(str(40 + random.randint(10, 30)))},
                        {"description": "Luxury Accommodation Upgrade", "amount": Decimal(str(150 + random.randint(50, 150)))},
                        {"description": "Photography Service", "amount": Decimal(str(120 + random.randint(30, 80)))}
                    ]
                
                item = random.choice(item_choices)
                notes = f"For {trek['name']}" if random.random() < 0.5 else ""
                
                price_item = PriceItem.objects.create(
                    client=client,
                    description=item["description"],
                    amount=item["amount"],
                    notes=notes
                )
                print(f"  Created price item: {price_item.description} (${item['amount']})")
                
        except Exception as e:
            print(f"Error creating client {i}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"Successfully created {len(created_clients)} clients with related price items!")

if __name__ == "__main__":
    generate_test_data()