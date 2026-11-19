CREATE DATABASE aperio_research_catalog;

USE aperio_research_catalog;

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL, 
    email VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(30) NOT NULL, 
    last_name VARCHAR(30) NOT NULL,
    user_type ENUM(
        "Human", 
        "AI Agent"
    ) DEFAULT "Human",
    is_active BOOLEAN DEFAULT True,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INT,
    FOREIGN KEY (created_by)
        REFERENCES Users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) COMMENT = "Feature: User Management | Stores the credentials of individual users.";

CREATE TABLE Roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY, 
    role_title VARCHAR(30) NOT NULL UNIQUE, 
    role_description TEXT NOT NULL, 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    created_by INT NOT NULL,
    update_at TIMESTAMP, 
    updated_by INT,
    FOREIGN KEY (created_by)
        REFERENCES Users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (updated_by)
        REFERENCES Users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) COMMENT = "Feature: Role Management | Stores the information for different roles.";

CREATE TABLE Permissions (
    permission_id INT AUTO_INCREMENT PRIMARY KEY, 
    permission_name VARCHAR(30) NOT NULL UNIQUE,
    permission_description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    created_by INT NOT NULL,
    updated_at TIMESTAMP,
    updated_by INT,
    FOREIGN KEY (created_by)
        REFERENCES Users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE, 
    FOREIGN KEY (updated_by)
        REFERENCES Users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE 
) COMMENT = "Feature: Permission Management | Stores the permissions of the platform.";

CREATE TABLE RolesToPermissions (
    role_id INT NOT NULL, 
    permission_id INT NOT NULL,
    FOREIGN KEY (role_id) 
        REFERENCES Roles(role_id) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (permission_id)
        REFERENCES Permissions(permission_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
) COMMENT ="Feature: Role Management | Manages different permissions of a role.";

CREATE TABLE Research (
    research_id INT PRIMARY KEY AUTO_INCREMENT,
    started_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_by INT NOT NULL, 
    project_title VARCHAR(50), 
    description TEXT,
    FOREIGN KEY (started_by)
        REFERENCES Users(user_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) COMMENT = "Feature: Research | Provides information on a research project";

CREATE TABLE Deliverables (
    deliverable_id int NOT NULL UNIQUE,
    original_due TIMESTAMP,
    started_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_date TIMESTAMP,
    title VARCHAR(64),
    deliverable_desc TEXT,
    completion_status enum(
        "Complete",
        "In-progress",
        "Not started", 
        "Abandoned"
    ) NOT NULL,
    notes TEXT,
    research_id INT NOT NULL,
    FOREIGN KEY (research_id) 
        REFERENCES Research(research_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (research_id, deliverable_id)
) COMMENT = "Feature: Research | ";

CREATE TABLE TaskAssignment (
    user_id INT NOT NULL,
    deliverable_id INT NOT NULL,
    research_id INT NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES Users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (deliverable_id) 
        REFERENCES Deliverables(deliverable_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (research_id)
        REFERENCES Research(research_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (user_id, deliverable_id, research_id)
) COMMENT = "Feature: Research | Provides information on research tasks assigned to users";

CREATE TABLE Literature (
    doi VARCHAR(30) PRIMARY KEY, -- possibly create gen/spec to use ISBN as key in future
    title VARCHAR(64),
    source TEXT,
    relevant_deliverable INT,
    relevant_project int,
    FOREIGN KEY (relevant_deliverable) 
        REFERENCES Deliverables(deliverable_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (relevant_project)
        REFERENCES Deliverables(research_id)
        ON UPDATE CASCADE ON DELETE CASCADE
) COMMENT = "Feature: Research | Provides the collection of literatures used for a research task.";

CREATE TABLE Authors (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(64),
    last_name VARCHAR(64),
    profession VARCHAR(64), 
    reference TEXT
) COMMENT = "Features: Research | Provides the author information for each literature.";

CREATE TABLE Attribution (
    author_id INT NOT NULL,
    author_doi VARCHAR(30) NOT NULL, -- must match Literature.doi type
    FOREIGN KEY (author_id) 
        REFERENCES Authors(author_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (author_doi) 
        REFERENCES Literature(doi) -- see literature table
        ON UPDATE CASCADE ON DELETE CASCADE
) COMMENT = "Features: Research | Maps a resercher and their work.";

CREATE TABLE ExperimentDetails (
    experiment_id INT AUTO_INCREMENT,
    research_id INT NOT NULL,
    experiment_title VARCHAR(45),
    experiment_desc TEXT,
    experiment_method TEXT,
    FOREIGN KEY (research_id)
        REFERENCES Research(research_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (experiment_id, research_id) -- AUTO_INCREMENT column must come first
) COMMENT = "Feature: Research | Provides information on experiment conducted
             for a research.";

CREATE TABLE ExperimentResults (
    result_id INT AUTO_INCREMENT,
    experiment_id INT NOT NULL,
    research_id INT NOT NULL,
    FOREIGN KEY (research_id)
        REFERENCES Research(research_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (experiment_id)
        REFERENCES ExperimentDetails(experiment_id)
        ON DELETE CASCADE ON UPDATE CASCADE,  
    PRIMARY KEY (result_id, research_id, experiment_id)
) COMMENT = "Feature: Research | Provides the result of each experiment run";


CREATE TABLE PIIPolicies (
    policy_id INT PRIMARY KEY AUTO_INCREMENT,
    policy_title VARCHAR(64),
    policy_description TEXT,
    procedure_name VARCHAR(64)
) COMMENT = "Feature: Logs | Policies to handle PII. 
            The policy_desciption contains what the system uses to
            recognize a PII to be redacted or tokenized. The procedure_name
            is a handler procedure for the policy.";

CREATE TABLE QueryLog (
    query_id INT PRIMARY KEY AUTO_INCREMENT,
    query_text TEXT,
    query_type ENUM (
        "CREATE",
        "UPDATE", 
        "DELETE", 
        "SELECT",
        "ROLLBACK", 
        "INSERT"
    ),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    created_by INT NOT NULL, 
    FOREIGN KEY (created_by)
        REFERENCES Users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
) COMMENT = "Feature: Logs | Each query and transaction close is 
             is logged into the system, and redacted accordingly.";


CREATE TABLE DataChangeLog (
    old_data TEXT,
    updated_data TEXT,
    query_id INT NOT NULL,
    relevant_pii INT,
    result_id INT NOT NULL,
    experiment_id INT NOT NULL,
    research_id INT NOT NULL,
    FOREIGN KEY (query_id)
        REFERENCES QueryLog(query_id)
        ON UPDATE CASCADE ON DELETE RESTRICT, 
    FOREIGN KEY (experiment_id)
        REFERENCES ExperimentDetails(experiment_id)
        ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (research_id)
        REFERENCES Research(research_id)
        ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (result_id)
        REFERENCES ExperimentResults(result_id)
        ON DELETE CASCADE ON UPDATE CASCADE
)   COMMENT = "Feature: Logs | Logs all of the changes to data. 
               Including being added or deleted. Redacted accordingly.";