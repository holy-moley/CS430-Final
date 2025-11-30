
USE `lib`;
DROP PROCEDURE checkout_book;

DELIMITER //

CREATE PROCEDURE checkout_book(IN inputBookID VARCHAR(7), IN inputUserID INT, OUT outputMsg VARCHAR(50))
BEGIN
	SELECT 
    @available := BookAvailable
    FROM books
    WHERE BookID = inputBookID;

IF  @available > 0

THEN
	SELECT
		@checkoutID := MAX(CheckoutID) +1
	FROM book_checkouts;
    
	UPDATE books SET BookAvailable = BookAvailable - 1 
    WHERE BookID = inputBookID;
    
	INSERT INTO `book_checkouts` (`CheckoutID`, `idUsers`, `BookID`, `CheckoutDate`, `ReturnDate`) 
	VALUES (@checkoutID, inputUserID, inputBookID, NOW(), '2025-12-5');
    SET outputMsg = "Success!";
ELSE 
	SET outputMSG = "Book unavailable!";
END IF;
END //

