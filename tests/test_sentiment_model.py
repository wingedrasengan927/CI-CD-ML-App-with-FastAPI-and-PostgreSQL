import pytest

from sentiment_model_inference import get_sentiment

@pytest.fixture(params = [
    "I had a great experience! will definitely visit again",
    "Wonderful.",
    "The staff here are very helpful; This has become my go to store.",
    "I got everything I wanted. Great!",
    "I love the atmosphere here - pleasant and beautifull"])
def positive_reviews(request):
    yield request.param

@pytest.fixture(params=[
    "Worst Experience!",
    "I didn't get what I was looking for. I'm never coming back here",
    "Waste of time!",
    "Worst service, worst ambience, worst everything!",])
def negative_reviews(request):
    yield request.param

def test_postive_reviews(positive_reviews):
    assert get_sentiment(positive_reviews) > 0

def test_negative_reviews(negative_reviews):
    assert get_sentiment(negative_reviews) < 0 