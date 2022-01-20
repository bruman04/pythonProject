from Chat import *

starHTML: str = r"""<span class="fa fa-star checked"></span>"""
noStarHTML: str = r"""<span class="fa fa-star"></span>"""


# Done by Ng Rong Kai:

class Review(Message):

    # Inheritance & Polymorphism.
    def __init__(
            self,
            sender_id: str = '',
            review: str = '',
            timestamp: int = 0,
            edited: bool = False,
            timeoffset: int = 8,
            stars: int = 3
    ):
        super().__init__(sender_id, review, timestamp, edited, timeoffset)
        self.review = self.message.strip()
        self.stars = int(round(stars if 1 <= stars <= 5 else 3))

    def rvw(self) -> str:
        self.review = self.msg().strip()
        return self.review.strip()

    def edit(self, new_review: str = '', new_stars: int = 3):
        super().edit(new_review.strip())
        self.review = self.rvw()
        self.edited: bool = self.edited if self.stars == new_stars else True
        self.stars = int(round(new_stars if 1 <= new_stars <= 5 else 3))
        return self

    def delete(self):
        super().delete()
        self.review = self.rvw()
        self.stars = 0
        return self

    def editReview(self, new_review: str = ''):
        return self.edit(new_review, self.rating())

    def rating(self):
        self.stars = int(round(self.stars if 1 <= self.stars <= 5 else 3))
        return self.stars

    def starsString(self):
        return (r'★' * self.rating() + r'☆' * abs(5 - self.rating()))[:5].strip()

    def starsHTML(self):
        return (starHTML * self.rating() + noStarHTML * abs(5 - self.rating())).strip()

    def editStars(self, new_stars: int = 3):
        return self.edit(self.rvw(), new_stars)

    def reply(
            self,
            replyer_id: str = '',
            reply: str = '',
            timeoffset: int = 8,
            stars: int = 3
    ):
        return Review(
            sender_id=replyer_id,
            review=f"(Replying to {self.id()})\n{reply}".strip(),
            timeoffset=timeoffset,
            stars=stars
        )

    def __str__(self) -> str:
        return self.starsString() + '\n' + self.rvw()


# Done by Ng Rong Kai:

class Feedback(Chat):

    # Inheritance & Polymorphism.
    def __init__(self, product_id: str = '', vendor_id: str = '', db: str = "review.db"):
        super().__init__(product_id, vendor_id, db.strip())
        self.product_id: str = self.customer_id

    def getLastReviewObject(self) -> Review:
        C: list[Review] = self.getFeedback()
        return C[-1] if C else Review().delete()

    def getReviewsCount(self) -> int:
        return len(self.getFeedback())

    def getFeedbacksByVendorID(self, vendor_id: str) -> set[str]:
        """
        This method returns a vendor's set of product_id(s) for reviews and feedback only.
        This does not necessarily return all of a vendor's products.
        :param vendor_id: The Vendor's ID.
        :return: A set of feedback's product_id(s) belonging to the vendor.
        """
        reviews: set = set()
        reviewdb = open(self.db, 'c')
        for k in reviewdb:
            k = k.split('|')
            k = k[0], k[-1]
            if k[-1] == vendor_id:
                reviews.add(k[0])
        reviewdb.close()
        return reviews

    def getFeedback(self) -> list[Review]:
        reviewdb = open(self.db, 'c')
        if self.chatKey in reviewdb:
            feedback = reviewdb[self.chatKey]
        else:
            feedback = reviewdb[self.chatKey] = []
        reviewdb.close()
        return feedback

    def setFeedback(self, feedback: list[Review]) -> bool:
        reviewdb = open(self.db, 'c')
        try:
            reviewdb[self.chatKey] = feedback
        except:
            return False
        finally:
            reviewdb.close()
        return True

    def delFeedback(self) -> bool:
        reviewdb = open(self.db, 'c')
        try:
            reviewdb.pop(self.chatKey)
            try:
                del reviewdb[self.chatKey]
            except:
                pass
            del self
        except:
            return False
        finally:
            reviewdb.close()
        return True

    def appendMultiFeedback(self, reviewObjects: list[Review]) -> bool:
        return self.setFeedback(self.getFeedback() + [
            r for r in reviewObjects if r.review.strip() and 1 <= r.stars <= 5 and isinstance(r.stars, int)
        ])

    def appendFeedbackReview(self, user_id: str, review: str, stars: int, utcTimezone: int = 8) -> bool:
        if review.strip() and 1 <= stars <= 5:
            c: list[Review] = self.getFeedback()
            c.append(Review(
                sender_id=user_id,  # Unlike chat, anyone can add a feedback or review.
                review=review.strip(),
                stars=int(round(stars)),
                timeoffset=utcTimezone
            ))
            return self.setFeedback(c)
        return False

    def insertFeedbackReview(self, message_index: int, user_id: str, review: str, stars: int,
                             utcTimezone: int = 8) -> bool:
        if review.strip() and 1 <= stars <= 5:
            c: list[Review] = self.getFeedback()
            c.insert(message_index + 1, Review(
                sender_id=user_id,  # Unlike chat, anyone can place a feedback or review.
                review=review.strip(),
                stars=int(round(stars)),
                timeoffset=utcTimezone
            ))
            return self.setFeedback(c)
        return False

    def replyFeedbackReview(self, replying_message_index: int, replyer_id: str, reply: str, stars: int,
                            utcTimezone: int = 8) -> bool:
        if reply.strip() and 1 <= stars <= 5:
            c: list[Review] = self.getFeedback()
            try:
                c.insert(replying_message_index + 1, c[replying_message_index].reply(
                    replyer_id=replyer_id,  # Unlike chat, anyone can reply a feedback or review.
                    reply=reply.strip(),
                    stars=int(round(stars)),
                    timeoffset=utcTimezone
                ))
            except IndexError:  # Replying message doesn't exist!
                return False
            return self.setFeedback(c)
        return False

    def editFeedbackReview(self, review_index: int, new_review: str, new_stars: int) -> bool:
        if new_review.strip() and 1 <= new_stars <= 5:
            c: list[Review] = self.getFeedback()
            try:
                c[review_index] = c[review_index].edit(new_review.strip(), new_stars)
            except IndexError:
                return False
            return self.setFeedback(c)
        return self.delFeedbackReview(review_index)

    def editFeedbackReviewMessage(self, review_index: int, new_review: str) -> bool:
        if new_review.strip():
            c: list[Review] = self.getFeedback()
            try:
                c[review_index] = c[review_index].editReview(new_review.strip())
            except IndexError:
                return False
            return self.setFeedback(c)
        return self.delFeedbackReview(review_index)

    def editFeedbackReviewStars(self, review_index: int, new_stars: int) -> bool:
        if 1 <= new_stars <= 5:
            c: list[Review] = self.getFeedback()
            try:
                c[review_index] = c[review_index].editStars(new_stars)
            except IndexError:
                return False
            return self.setFeedback(c)
        return self.delFeedbackReview(review_index)

    def delFeedbackReview(self, review_index: int) -> bool:
        C: list[Review] = self.getFeedback()
        try:
            del C[review_index]
        except IndexError:
            return False
        return self.setFeedback(C)

    def getOverallRating(self) -> float:
        fb: tuple[int] = tuple(r.rating() for r in self.getFeedback())
        try:
            overallRating: float = sum(fb) / len(fb)
        except ZeroDivisionError:
            return 0.00  # In case there are no reviews.
        if overallRating < 1.0:
            overallRating = 1.0
        elif overallRating > 5.0:
            overallRating = 5.0
        return round(abs(overallRating), 2)

# Done by Ng Rong Kai.
