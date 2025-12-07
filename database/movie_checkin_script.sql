USE `lib`;
DROP PROCEDURE IF EXISTS checkin_movie;

DELIMITER //

CREATE PROCEDURE checkin_movie(IN inputMovieID INT, IN inputUserID varchar(100))
BEGIN
SET @checkout_movie_entry = NULL;
SELECT
	@checkout_movie_entry := CheckoutID
    FROM movie_checkouts
    WHERE MovID = inputMovieID AND idUsers = inputUserID
    ORDER BY CheckoutDate DESC;
IF  @checkout_movie_entry IS NOT NULL
THEN

	DELETE FROM movie_checkouts WHERE CheckoutID = @checkout_movie_entry;
    
	UPDATE movies SET MovAvailable = MovAvailable + 1 
    WHERE MovID = inputMovieID;
    
    SET @outputMsg = "Movie checked in!";
ELSE 
	SET @outputMsg = "This user has not checked out this movie!";
END IF;
END //