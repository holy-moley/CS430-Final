
USE `lib`;
DROP PROCEDURE IF EXISTS checkout_movie;

DELIMITER //

CREATE PROCEDURE checkout_movie(IN inputMovieID INT, IN inputUserID varchar(100))
BEGIN
	SELECT 
    @available := MovAvailable
    FROM movies
    WHERE MovID = inputMovieID;

IF  @available > 0

THEN
	SELECT
		@checkoutID := MAX(CheckoutID) +1
	FROM movie_checkouts;
    
	UPDATE movies SET MovAvailable = MovAvailable - 1 
    WHERE MovID = inputMovieID;
    
	INSERT INTO `movie_checkouts` (`CheckoutID`, `idUsers`, `MovID`, `CheckoutDate`, `ReturnDate`) 
	VALUES (@checkoutID, inputUserID, inputMovieID, CURDATE(), CURDATE() + INTERVAL 1 WEEK);
    SET @outputMsg = "Movie checked out!";
ELSE 
	SET @outputMsg = "Movie unavailable!";
END IF;
END //