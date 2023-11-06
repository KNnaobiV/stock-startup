from django.contrib.auth.mixins import UserPassesTestMixin

class SupervisorTest(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.filter(is_manager=True)