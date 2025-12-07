
USE `lib`;
DROP PROCEDURE IF EXISTS checkout_book;

DELIMITER //

CREATE PROCEDURE checkout_book(IN inputBookID INT, IN inputUserID INT)
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
	VALUES (@checkoutID, inputUserID, inputBookID, CURDATE(), CURDATE() + INTERVAL 1 WEEK);
    SET @outputMsg = "Book checked out!";
ELSE 
	SET @outputMsg = "Book unavailable!";
END IF;
END //

