import pandas as pd

# Load the CSV file
df = pd.read_csv("./laptops.csv")


# Initialize dictionaries to keep track of unique entities and their IDs
brand_ids = {}
cpu_brand_ids = {}
gpu_brand_ids = {}
os_ids = {}
warranty_policy_ids = {}
current_brand_id = current_cpu_brand_id = current_gpu_brand_id = current_os_id = (
    current_warranty_id
) = 1

# Initialize the list of SQL statements
sql_statements = []

# Process brands, cpu brands, gpu brands, OS, and warranty policies
for i, row in df.iterrows():
    # Brands
    brand = row["brand"]
    if brand not in brand_ids:
        brand_ids[brand] = current_brand_id
        sql_statements.append(
            f"INSERT INTO brand (brand_id, brand_name) VALUES ({current_brand_id}, '{brand}');"
        )
        current_brand_id += 1
for i, row in df.iterrows():
    # CPU Brands
    cpu_brand = row["processor_brand"]
    if cpu_brand not in cpu_brand_ids:
        cpu_brand_ids[cpu_brand] = current_cpu_brand_id
        sql_statements.append(
            f"INSERT INTO cpu_brand (cpu_brand_id, cpu_brand_name) VALUES ({current_cpu_brand_id}, '{cpu_brand}');"
        )
        current_cpu_brand_id += 1
for i, row in df.iterrows():
    # GPU Brands
    gpu_brand = row["gpu_brand"]
    if gpu_brand not in gpu_brand_ids:
        gpu_brand_ids[gpu_brand] = current_gpu_brand_id
        sql_statements.append(
            f"INSERT INTO gpu_brand (gpu_brand_id, gpu_brand_name) VALUES ({current_gpu_brand_id}, '{gpu_brand}');"
        )
        current_gpu_brand_id += 1
for i, row in df.iterrows():
    # OS
    os = row["OS"]
    if os not in os_ids:
        os_ids[os] = current_os_id
        sql_statements.append(
            f"INSERT INTO os (os_id, os_name) VALUES ({current_os_id}, '{os}');"
        )
        current_os_id += 1
for i, row in df.iterrows():
    # Warranty Policies
    year_of_warranty = row["year_of_warranty"]
    if year_of_warranty == "No information":
        continue
    if year_of_warranty not in warranty_policy_ids:
        warranty_policy_ids[year_of_warranty] = current_warranty_id
        if not year_of_warranty.isdigit():
            year_of_warranty = f"'{year_of_warranty}'"
        sql_statements.append(
            f"INSERT INTO warranty_policy (warranty_policy_id, year_of_warranty) VALUES ({current_warranty_id}, {year_of_warranty});"
        )
        current_warranty_id += 1

dml_statements = sql_statements
current_laptop_id = current_cpu_id = current_gpu_id = current_ram_id = (
    current_storage_1_id
) = current_storage_2_id = current_screen_id = 1

cpu = {}
for i, row in df.iterrows():
    id = (
        row["processor_brand"],
        row["processor_tier"],
        row["num_cores"],
        row["num_threads"],
    )
    if id not in cpu:
        cpu[id] = current_cpu_id
        dml_statements.append(
            f"INSERT INTO cpu (cpu_id, cpu_brand_id, processor_brand, processor_tier, num_cores, num_threads, model, gpu_type) VALUES ({current_cpu_id}, {cpu_brand_ids[row['processor_brand']]}, '{row['processor_brand']}', '{row['processor_tier']}', {row['num_cores']}, {row['num_threads']}, NULL, '{row['gpu_type']}');"
        )
        current_cpu_id += 1

gpu = {}
for i, row in df.iterrows():
    gpu_brand = row["gpu_brand"]
    gpu_type = row["gpu_type"]
    id = (gpu_brand, gpu_type)
    if id not in gpu:
        gpu[id] = current_gpu_id
        dml_statements.append(
            f"INSERT INTO gpu (gpu_id, gpu_brand_id, gpu_type,model) VALUES ({current_gpu_id}, {gpu_brand_ids[gpu_brand]}, '{gpu_type}', NULL);"
        )
        current_gpu_id += 1

rams = {}
for i, row in df.iterrows():
    if row["ram_memory"] not in rams:
        rams[row["ram_memory"]] = current_ram_id
        dml_statements.append(
            f"INSERT INTO ram (ram_id, ram_memory, model) VALUES ({current_ram_id}, {row['ram_memory']}, NULL);"
        )
        current_ram_id += 1


s1 = {}
for i, row in df.iterrows():
    # Insert into Storage_1
    primary_storage_type = row["primary_storage_type"]
    primary_storage_capacity = row["primary_storage_capacity"]
    id = (primary_storage_type, primary_storage_capacity)
    if id not in s1:
        s1[id] = current_storage_1_id
        dml_statements.append(
            f"INSERT INTO storage_1 (storage_1_id, primary_storage_type, primary_storage_capacity, model) VALUES ({current_storage_1_id}, '{primary_storage_type}', {primary_storage_capacity}, NULL);"
        )
        current_storage_1_id += 1


s2 = {}
for i, row in df.iterrows():
    # Insert into Storage_2 if applicable
    if row["secondary_storage_type"].lower() != "no secondary storage":
        secondary_storage_type = row["secondary_storage_type"].lower()
        secondary_storage_capacity = row["secondary_storage_capacity"]
        id = (secondary_storage_type, secondary_storage_capacity)
        if id not in s2:
            s2[id] = current_storage_2_id
            dml_statements.append(
                f"INSERT INTO storage_2 (storage_2_id, secondary_storage_type, secondary_storage_capacity, model) VALUES ({current_storage_2_id}, '{secondary_storage_type}', {secondary_storage_capacity}, NULL);"
            )
            current_storage_2_id += 1


screens = {}
for i, row in df.iterrows():
    id = (row["display_size"], row["resolution_width"], row["resolution_height"])
    if id not in screens:
        screens[id] = current_screen_id
        # Insert into Screens
        dml_statements.append(
            f"INSERT INTO screen (screen_id, display_size, resolution_width, resolution_height, model, is_touch_screen) VALUES ({current_screen_id}, {row['display_size']}, {row['resolution_width']}, {row['resolution_height']}, NULL, {row['is_touch_screen']});"
        )
        current_screen_id += 1


# Append statements for laptops and their components
for i, row in df.iterrows():
    # Insert into laptops
    cpu_id = cpu[
        (
            row["processor_brand"],
            row["processor_tier"],
            row["num_cores"],
            row["num_threads"],
        )
    ]
    gpu_id = gpu[(row["gpu_brand"], row["gpu_type"])]
    ram_id = rams[row["ram_memory"]]
    s1_id = s1[row["primary_storage_type"], row["primary_storage_capacity"]]
    if row["secondary_storage_type"].lower() == "no secondary storage":
        s2_id = "NULL"
    else:
        s2_id = s2[
            row["secondary_storage_type"].lower(), row["secondary_storage_capacity"]
        ]
    screen_id = screens[
        (row["display_size"], row["resolution_width"], row["resolution_height"])
    ]
    os_id = os_ids[row["OS"]]
    if row["year_of_warranty"] == "No information":
        warranty_policy_id = "NULL"
    else:
        warranty_policy_id = warranty_policy_ids[row["year_of_warranty"]]
    dml_statements.append(
        f"INSERT INTO laptop (laptop_id, brand_id, model, price, cpu_id, gpu_id, ram_id, storage_1_id, storage_2_id, screen_id, os_id, warranty_policy_id) VALUES ({current_laptop_id}, {brand_ids[row['brand']]}, '{row['Model']}', {row['Price']}, {cpu_id}, {gpu_id}, {ram_id}, {s1_id}, {s2_id}, {screen_id}, {os_id}, {warranty_policy_id});"
    )
    current_laptop_id += 1


with open("dml.sql", "w") as f:
    f.write("\n".join(dml_statements))
