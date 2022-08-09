drop table clients;
--@block
CREATE TABLE Clients(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    client_email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
--@block
CREATE TABLE Reservations(
    id INT AUTO_INCREMENT PRIMARY KEY,
    reservation_date DATE NOT NULL,
    reservation_time INT NOT NULL,
    court_number INT NOT NULL,
    client_email VARCHAR(255) NOT NULL,
    FOREIGN KEY (client_email) REFERENCES Clients (client_email) ON DELETE CASCADE ON UPDATE CASCADE
);