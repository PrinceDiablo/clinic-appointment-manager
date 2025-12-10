-- MySQL schema for Clinic Appointment Manager

-- Users and User Details

CREATE TABLE  IF NOT EXISTS `users` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `password_hash` VARCHAR(255) NOT NULL,
    `contact_no` VARCHAR(30),
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `last_login` TIMESTAMP NULL DEFAULT NULL,
    `failed_logins` INT NOT NULL DEFAULT 0,
    `locked_until` TIMESTAMP NULL DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_users_user_name` (`user_name`),
    UNIQUE KEY `uq_users_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `user_details` (
    `user_id` INT UNSIGNED NOT NULL,
    `name` VARCHAR(255),
    `dob` DATE,
    `gender` ENUM('M','F','O'),
    `address_line1` VARCHAR(255),
    `address_line2` VARCHAR(255),
    `city` VARCHAR(100),
    `state` VARCHAR(100),
    `postal_code` VARCHAR(20),
    `country` VARCHAR(100),
    PRIMARY KEY (`user_id`),
    CONSTRAINT `fk_ud_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- RBAC (Roles + Permissions)

CREATE TABLE IF NOT EXISTS `roles` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(60) NOT NULL,
    `description` VARCHAR(255),
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_roles_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `permissions` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL,
    `description` VARCHAR(255),
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_permissions_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `role_permissions` (
    `role_id` INT UNSIGNED NOT NULL,
    `permission_id` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`role_id`,`permission_id`),
    CONSTRAINT `fk_rp_role` FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_rp_permission` FOREIGN KEY (`permission_id`) REFERENCES `permissions`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `user_roles` (
    `user_id` INT UNSIGNED NOT NULL,
    `role_id` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`user_id`,`role_id`),
    CONSTRAINT `fk_ur_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    CONSTRAINT `fk_ur_role` FOREIGN KEY (`role_id`) REFERENCES `roles`(`id`) ON DELETE CASCADE,
    INDEX `idx_ur_role` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Password change

CREATE TABLE IF NOT EXISTS `password_changes` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL,
    `token` CHAR(60) NOT NULL,
    `expires_at` TIMESTAMP NOT NULL,
    `used` TINYINT(1) NOT NULL DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE KEY `uq_pc_token` (`token`),
    CONSTRAINT `fk_pc_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    INDEX `idx_pc_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Doctors Table

CREATE TABLE IF NOT EXISTS `doctor_details` (
    `user_id` INT UNSIGNED NOT NULL,
    `specialization` VARCHAR(255) NOT NULL,
    `licence_no` VARCHAR(100) NOT NULL,
    `fees` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `uq_doctor_licence_no` (`licence_no`),
    CONSTRAINT `fk_dd_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    INDEX `idx_dd_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `doctor_availability` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` INT UNSIGNED NOT NULL,
    `day` ENUM('MON','TUE','WED','THU','FRI','SAT','SUN') NOT NULL,
    `start_time` TIME NOT NULL,
    `slot_duration_minutes` INT UNSIGNED NOT NULL DEFAULT 60,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_da_user` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    INDEX `idx_da_user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Appointments Table

CREATE TABLE IF NOT EXISTS `appointments` (
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `patient_id` INT UNSIGNED NOT NULL,
    `doctor_id` INT UNSIGNED NOT NULL,
    `appointment_timestamp` TIMESTAMP NOT NULL,
    `arrival_timestamp` TIMESTAMP NULL DEFAULT NULL,
    `status` ENUM('requested','confirmed','cancelled','completed','no_show') NOT NULL DEFAULT 'requested',
    `notes` TEXT,
    `created_by_staff` INT UNSIGNED,
    `deleted_at` TIMESTAMP NULL DEFAULT NULL,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    CONSTRAINT `fk_appointments_patient` FOREIGN KEY (`patient_id`) REFERENCES `users`(`id`),
    CONSTRAINT `fk_appointments_doctor` FOREIGN KEY (`doctor_id`) REFERENCES `users`(`id`),
    CONSTRAINT `fk_appointments_staff` FOREIGN KEY (`created_by_staff`) REFERENCES `users`(`id`), 
    INDEX `idx_appointments_patient` (`patient_id`),
    INDEX `idx_appointments_doctor` (`doctor_id`),
    INDEX `idx_appointments_staff` (`created_by_staff`),
    INDEX `idx_appointments_at` (`appointment_timestamp`),
    INDEX `cidx_appointments_doctor_at` (`doctor_id`, `appointment_timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;