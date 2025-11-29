
USE `lib`;

DELIMITER //

CREATE PROCEDURE checkout_book(IN bookID VARCHAR(7), IN userID INT)
BEGIN
UPDATE books SET BookAvailable = BookAvailable - 1 
WHERE BookID = bookID AND BookAvailable > 0;

INSERT INTO `book_checkouts` (`CheckoutID`, `idUsers`, `BookID`, `CheckoutDate`, `ReturnDate`) 
VALUES ('1', userID, bookID, NOW(), '2025-12-5')
WHERE BookID = bookID AND BookAvailable > 0;
END //
