""" 
william lee flight_booking_system.py
simple flight booking system with booking and cancellation functionality
"""
from typing import Dict, Set
import unittest

class Flight:
    def __init__(self, flight_number, origin, destination, total_seats):
        self.flight_number = flight_number #str
        self.origin = origin #str
        self.destination = destination #str
        self.total_seats = total_seats #int
        self.available_seats = total_seats #int
        self._booked_passengers = set() #set w/ strings

    def book_seat(self, passenger_name):
        """
        book a seat for a passenger if available
        returns true on success, false otherwise
        """
        if self.available_seats <= 0:
            return False
        if passenger_name in self._booked_passengers:
            return False  #already booked
        self._booked_passengers.add(passenger_name)
        self.available_seats -= 1
        return True

    def cancel_booking(self, passenger_name):
        """
        cancel a passengers booking if it exists
        returns true on success, false otherwise
        """
        if passenger_name not in self._booked_passengers:
            return False
        self._booked_passengers.remove(passenger_name)
        self.available_seats += 1
        return True

    def get_available_seats(self) -> int:
        """
        return # of available seats
        """
        return self.available_seats


class BookingSystem:
    def __init__(self):
        #internal mapping from flight numbers to flight instances
        self._flights = {} #dictionary for mapping each flights unique ID (the flight number string) to its Flight instance
        #so we know what to refer to

    def add_flight(self, flight):
        """
        add a flight to the system, raises value error if flight already exists
        """
        if flight.flight_number in self._flights:
            raise ValueError(f"Flight {flight.flight_number} already exists.")
        self._flights[flight.flight_number] = flight

    def book_flight(self, flight_number, passenger_name):
        """
        book a seat on the specified flight, returns true on success, false otherwise
        """
        flight = self._flights.get(flight_number)
        if not flight:
            return False
        return flight.book_seat(passenger_name)

    def cancel_booking(self, flight_number, passenger_name):
        """
        cancel a booking on the specified flight, returns true on success, false otherwise
        """
        flight = self._flights.get(flight_number)
        if not flight:
            return False
        return flight.cancel_booking(passenger_name)


#testing functionality
class TestFlight(unittest.TestCase):
    def setUp(self):
        self.flight = Flight("BA123", "Seattle", "New York", 2)

    def test_initial_seats(self):
        self.assertEqual(self.flight.get_available_seats(), 2)

    def test_successful_booking(self):
        result = self.flight.book_seat("Alice")
        self.assertTrue(result)
        self.assertEqual(self.flight.get_available_seats(), 1)

    def test_overbooking(self):
        self.flight.book_seat("Alice")
        self.flight.book_seat("Bob")
        result = self.flight.book_seat("Charlie")
        self.assertFalse(result)
        self.assertEqual(self.flight.get_available_seats(), 0)

    def test_duplicate_booking(self):
        self.flight.book_seat("Alice")
        result = self.flight.book_seat("Alice")
        self.assertFalse(result)
        self.assertEqual(self.flight.get_available_seats(), 1)

    def test_successful_cancellation(self):
        self.flight.book_seat("Alice")
        result = self.flight.cancel_booking("Alice")
        self.assertTrue(result)
        self.assertEqual(self.flight.get_available_seats(), 2)

    def test_invalid_cancellation(self):
        result = self.flight.cancel_booking("Bob")
        self.assertFalse(result)
        self.assertEqual(self.flight.get_available_seats(), 2)


class TestBookingSystem(unittest.TestCase):
    def setUp(self):
        self.system = BookingSystem()
        self.flight1 = Flight("BA123", "Seattle", "New York", 1)
        self.flight2 = Flight("BA456", "Seattle", "London", 1)
        self.system.add_flight(self.flight1)
        self.system.add_flight(self.flight2)

    def test_add_existing_flight(self):
        with self.assertRaises(ValueError):
            self.system.add_flight(self.flight1)

    def test_book_and_cancel(self):
        # Book on BA123
        self.assertTrue(self.system.book_flight("BA123", "Alice"))
        self.assertFalse(self.system.book_flight("BA123", "Bob"))  # no seats left
        # Cancel and rebook
        self.assertTrue(self.system.cancel_booking("BA123", "Alice"))
        self.assertTrue(self.system.book_flight("BA123", "Bob"))

    def test_invalid_flight(self):
        self.assertFalse(self.system.book_flight("UNKNOWN", "Alice"))
        self.assertFalse(self.system.cancel_booking("UNKNOWN", "Alice"))


if __name__ == "__main__":
    """
    unit tests,
    TestFlight: initial seat count, booking success/failure, duplicate bookings, cancellations
    TestBookingSystem: adding flights, booking/cancelling across flights, invalid flight handling
    """
    unittest.main(exit=False) #run tests but dont exit @end 

    #example usage to see results printed below
    print("\n--- Example Usage Outputs ---")

    #sample flights
    flight_ke = Flight("KE001", "Seoul", "Los Angeles", 2) #2 seats
    flight_dl = Flight("DL002", "Atlanta", "Paris", 1) #1 seat
    flight_ca = Flight("CA003", "Beijing", "Sydney", 3) #3 seats

    system = BookingSystem()
    system.add_flight(flight_ke)
    system.add_flight(flight_dl)
    system.add_flight(flight_ca)

    #bookings
    print("Booking KE001 for Connor McGregor:", system.book_flight("KE001", "Connor McGregor")) #true since seats are still available
    print("Booking KE001 for Floyd Mayweather:", system.book_flight("KE001", "Floyd Mayweather")) #true since seats are still available
    print("Booking KE001 for Mike Tyson:", system.book_flight("KE001", "Mike Tyson")) #false since we ran out

    print("Cancel KE001 for Floyd Mayweather:", system.cancel_booking("KE001", "Floyd Mayweather")) #true on success
    print("Booking KE001 for Mike Tyson:", system.book_flight("KE001", "Mike Tyson")) #true since we got seats again

    #bookings
    print("Booking DL002 for Jon Jones:", system.book_flight("DL002", "Jon Jones")) #true since 1 seat left
    print("Booking DL002 for Bruce Lee:", system.book_flight("DL002", "Bruce Lee")) #false since none left

    #bookings
    print("Booking CA003 for Bruce Lee:", system.book_flight("CA003", "Bruce Lee")) #true since seats are still available
    print("Booking CA003 for Mike Tyson:", system.book_flight("CA003", "Mike Tyson"))  #true since seats are still available
    print("Seats left on CA003:", flight_ca.get_available_seats()) #return the last seat 