USE eventra_db;

INSERT INTO users (name, email, phone, password, role) VALUES
('Admin', 'admin@eventra.com', '9999999999', 'admin123', 'admin'),
('Rahul Sharma', 'rahul@example.com', '9876543210', 'pass123', 'user'),
('Priya Verma', 'priya@example.com', '9876543211', 'pass123', 'user');

INSERT INTO events (event_name, category, description, venue, city, event_date, start_time, total_seats, available_seats, ticket_price, organizer_id) VALUES
('Tech Fest 2025', 'Technology', 'Annual technology festival', 'Convention Hall', 'Delhi', '2025-03-15', '10:00:00', 200, 200, 499.00, 1),
('Music Night', 'Music', 'Live band performance', 'Open Grounds', 'Mumbai', '2025-03-20', '18:00:00', 150, 150, 799.00, 1),
('Startup Summit', 'Business', 'Meet investors and founders', 'Hotel Grand', 'Bangalore', '2025-04-05', '09:00:00', 100, 100, 999.00, 1),
('Comedy Show', 'Entertainment', 'Stand-up comedy evening', 'City Auditorium', 'Pune', '2025-03-25', '19:00:00', 80, 80, 599.00, 1);
