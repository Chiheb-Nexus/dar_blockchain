from rest_framework import permissions


class BlacklistPermission(permissions.BasePermission):
	"""
	Global permission check for blacklisted IPs.
	"""

	def has_permission(self,request, view, obj=None):
		ip_addr = request.META['REMOTE_ADDR']
		print(ip_addr)
		#blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
		return True
class AllowAny(permissions.BasePermission):
	'''
	for register API
	'''
	def has_permission(self,request,view):
		if(request.is_ajax):
			print(request.META['HTTP_USER_AGENT'])
			return True
		else:
			print('is not ajax')
		return True