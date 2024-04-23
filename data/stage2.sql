DROP TABLE IF EXISTS gpu_brand;
DROP TABLE IF EXISTS cpu_brand;
DROP TABLE IF EXISTS brand;
DROP TABLE IF EXISTS warranty_policy;
DROP TABLE IF EXISTS os;
DROP TABLE IF EXISTS screen;
DROP TABLE IF EXISTS storage_2;
DROP TABLE IF EXISTS storage_1;
DROP TABLE IF EXISTS ram;
DROP TABLE IF EXISTS gpu;
DROP TABLE IF EXISTS cpu;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS laptop;

-- Brand Entity
CREATE TABLE brand (
    brand_id SERIAL PRIMARY KEY,
    brand_name VARCHAR(255) UNIQUE NOT NULL
);

-- CPU Brand Entity
CREATE TABLE cpu_brand (
    cpu_brand_id SERIAL PRIMARY KEY,
    cpu_brand_name VARCHAR(255) UNIQUE NOT NULL
);

-- GPU Brand Entity
CREATE TABLE gpu_brand (
    gpu_brand_id SERIAL PRIMARY KEY,
    gpu_brand_name VARCHAR(255) UNIQUE NOT NULL
);

-- Laptop Entity
CREATE TABLE laptop (
    laptop_id SERIAL PRIMARY KEY,
    brand_id INT NOT NULL,
    model VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (brand_id) REFERENCES brand(brand_id),
    UNIQUE (brand_id, model)
);

-- Rating Entity
CREATE TABLE rating (
    rating_id SERIAL PRIMARY KEY,
    laptop_id INT NOT NULL,
    rating DECIMAL(3,2),
    FOREIGN KEY (laptop_id) REFERENCES laptop(laptop_id)
);

-- CPU Entity
CREATE TABLE cpu (
    cpu_id SERIAL PRIMARY KEY,
    cpu_brand_id INT NOT NULL,
    processor_brand VARCHAR(255) NOT NULL,
    processor_tier VARCHAR(255) NOT NULL,
    num_cores INT NOT NULL,
    num_threads INT NOT NULL,
    model VARCHAR(255),
    gpu_type VARCHAR(255),
    FOREIGN KEY (cpu_brand_id) REFERENCES cpu_brand(cpu_brand_id),
    UNIQUE (processor_brand, processor_tier, num_cores, num_threads)
);

-- GPU Entity
CREATE TABLE gpu (
    gpu_id SERIAL PRIMARY KEY,
    gpu_brand_id INT NOT NULL,
    gpu_type VARCHAR(255) NOT NULL,
    model VARCHAR(255),
    FOREIGN KEY (gpu_brand_id) REFERENCES gpu_brand(gpu_brand_id),
    UNIQUE (gpu_brand_id, gpu_type)
);

-- RAM Entity
CREATE TABLE ram (
    ram_id SERIAL PRIMARY KEY,
    ram_memory INT NOT NULL,
    model VARCHAR(255),
    UNIQUE (ram_memory)
);

-- Storage_1 Entity
CREATE TABLE storage_1 (
    storage_1_id SERIAL PRIMARY KEY,
    primary_storage_type VARCHAR(255) NOT NULL,
    primary_storage_capacity INT NOT NULL,
    model VARCHAR(255),
    UNIQUE (primary_storage_type, primary_storage_capacity)
);

-- Storage_2 Entity
CREATE TABLE storage_2 (
    storage_2_id SERIAL PRIMARY KEY,
    secondary_storage_type VARCHAR(255),
    secondary_storage_capacity INT,
    model VARCHAR(255),
    UNIQUE (secondary_storage_type, secondary_storage_capacity)
);

-- Screen Entity
CREATE TABLE screen (
    screen_id SERIAL PRIMARY KEY,
    display_size DECIMAL(5,2) NOT NULL,
    resolution_width INT NOT NULL,
    resolution_height INT NOT NULL,
    model VARCHAR(255),
    is_touch_screen BOOLEAN NOT NULL,
    UNIQUE (display_size, resolution_width, resolution_height)
);

-- OS Entity
CREATE TABLE os (
    os_id SERIAL PRIMARY KEY,
    os_name VARCHAR(255) NOT NULL,
    model VARCHAR(255),
    UNIQUE (os_name)
);

-- Warranty Policy Entity
CREATE TABLE warranty_policy (
    warranty_policy_id SERIAL PRIMARY KEY,
    year_of_warranty INT NOT NULL,
    model VARCHAR(255),
    UNIQUE (year_of_warranty)
);

-- Laptop Components and Specifications Relationships
ALTER TABLE laptop ADD COLUMN cpu_id INT;
ALTER TABLE laptop ADD COLUMN gpu_id INT;
ALTER TABLE laptop ADD COLUMN ram_id INT;
ALTER TABLE laptop ADD COLUMN storage_1_id INT;
ALTER TABLE laptop ADD COLUMN storage_2_id INT DEFAULT NULL;
ALTER TABLE laptop ADD COLUMN screen_id INT;
ALTER TABLE laptop ADD COLUMN os_id INT;
ALTER TABLE laptop ADD COLUMN warranty_policy_id INT DEFAULT NULL;

ALTER TABLE laptop ADD FOREIGN KEY (cpu_id) REFERENCES cpu(cpu_id);
ALTER TABLE laptop ADD FOREIGN KEY (gpu_id) REFERENCES gpu(gpu_id);
ALTER TABLE laptop ADD FOREIGN KEY (ram_id) REFERENCES ram(ram_id);
ALTER TABLE laptop ADD FOREIGN KEY (storage_1_id) REFERENCES storage_1(storage_1_id);
ALTER TABLE laptop ADD FOREIGN KEY (storage_2_id) REFERENCES storage_2(storage_2_id);
ALTER TABLE laptop ADD FOREIGN KEY (screen_id) REFERENCES screen(screen_id);
ALTER TABLE laptop ADD FOREIGN KEY (os_id) REFERENCES os(os_id);
ALTER TABLE laptop ADD FOREIGN KEY (warranty_policy_id) REFERENCES warranty_policy(warranty_policy_id);

-- Unique constraints and indexes can be added here based on query requirements.
