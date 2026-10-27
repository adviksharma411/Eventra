USE eventra_db;

INSERT INTO users (name, email, phone, password, role) VALUES
('Admin',   'admin@eventra.com',   '9999999999', 'admin123',   'admin'),
('Advik',   'advik@example.com',   '8888888888', 'advik123',   'user'),
('Aayushi', 'aayushi@example.com', '7777777777', 'aayushi123', 'user');

INSERT INTO events
(event_name, category, description, venue, city, event_date, start_time,
 total_seats, available_seats, ticket_price, organizer_id, status) VALUES
('Music Night',   'Music',   'An evening of live music',    'Delhi Arena',           'Delhi',  '2026-05-20', '19:00:00', 100, 100, 500.00, 1, 'Active'),
('Tech Fest',     'Tech',    'Annual technology festival',  'Mumbai Convention Hall','Mumbai', '2026-06-01', '10:00:00',  50,  50, 800.00, 1, 'Active'),
('Food Carnival', 'Food',    'Street food festival',        'Delhi Haat',            'Delhi',  '2026-06-10', '12:00:00', 200, 200, 300.00, 1, 'Active'),
('Theatre Night', 'Theatre', 'Classic drama performance',   'Kamani Auditorium',     'Delhi',  '2026-06-15', '18:30:00',  80,  80, 400.00, 1, 'Active'),
('Marathon 10K',  'Sports',  'City marathon',               'Marine Drive',          'Mumbai', '2026-06-20', '06:00:00', 500, 500, 250.00, 1, 'Active');