
USE `lib`;
DROP PROCEDURE IF EXISTS checkin_book;

DELIMITER //

CREATE PROCEDURE checkin_book(IN inputBookID INT, IN inputUserID INT)
BEGIN
SET @checkout_book_entry = NULL;
SELECT
	@checkout_book_entry := CheckoutID
    FROM book_checkouts
    WHERE BookID = inputBookID AND idUsers = inputUserID
    ORDER BY CheckoutDate DESC;
IF  @checkout_book_entry IS NOT NULL
THEN

	DELETE FROM book_checkouts WHERE CheckoutID = @checkout_book_entry;
    
	UPDATE books SET BookAvailable = BookAvailable + 1 
    WHERE BookID = inputBookID;
    
    SET @outputMsg = "Book checked in!";
ELSE 
	SET @outputMsg = "This user has not checked out this book!";
END IF;
END //