-- EVIDENCE OF Transactions, Stored Procedures, and Triggers

-- 1. CONSTRAINTS
-- Ensure that for a specific trip, every rank_order is unique.
ALTER TABLE TRIP_LOCATIONS
ADD CONSTRAINT uk_trip_ranking UNIQUE (tripID, rank_order);

DELIMITER //

-- 2. STORED PROCEDURE
-- Handles the FIFO logic: If user has 5+ trips, delete the oldest.
-- Called explicitly by the application before insertion.
CREATE PROCEDURE sp_enforce_trip_cap(IN p_user_id INT)
BEGIN
    DECLARE trip_count INT;
    DECLARE oldest_trip_id INT;

    -- Check current number of trips for the user
    SELECT COUNT(*) INTO trip_count 
    FROM TRIP_PLANS 
    WHERE userID = p_user_id;

    -- If limit is reached or exceeded, remove the oldest
    IF trip_count >= 5 THEN
        SELECT tripID INTO oldest_trip_id
        FROM TRIP_PLANS
        WHERE userID = p_user_id
        ORDER BY tripID ASC
        LIMIT 1;

        DELETE FROM TRIP_PLANS WHERE tripID = oldest_trip_id;
    END IF;
END //

-- 3. TRIGGER
-- Ensures a trip cannot end before it starts.
CREATE TRIGGER trg_validate_trip_dates
BEFORE INSERT ON TRIP_PLANS
FOR EACH ROW
BEGIN
    IF NEW.endDate < NEW.startDate THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Integrity Error: Trip End Date cannot be before Start Date.';
    END IF;
END //

DELIMITER ;
