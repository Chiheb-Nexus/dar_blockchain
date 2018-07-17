

def user_is_active(func):
	def wrap (*args, **kwargs):
		return func()
	return wrap