class Booking:
    def __init__(self, name, email, phone, startDate, people, tourId=None, ref=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.startDate = startDate
        self.people = int(people)
        self.tourId = tourId
        self.ref = ref

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "startDate": self.startDate,
            "people": self.people,
            "tourId": self.tourId,
            "ref": self.ref,
        }

    @staticmethod
    def from_dict(data):
        return Booking(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            startDate=data.get("startDate"),
            people=data.get("people"),
            tourId=data.get("tourId"),
            ref=data.get("ref"),
        )