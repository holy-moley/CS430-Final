USE `lib`;

CALL checkout_book("B100", 100, @output);
SELECT @output;