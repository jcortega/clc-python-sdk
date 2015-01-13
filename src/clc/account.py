"""
Account related functions.  

These account related functions generally align one-for-one with published API calls categorized in the account category

API v1 - https://t3n.zendesk.com/forums/21509857-Account
API v2 - https://t3n.zendesk.com/forums/21645944-Account
"""

import clc

class Account:

	account_status_itos = { 1: 'Action', 2: 'Disabled', 3: 'Deleted', 4: 'Demo' }

	@staticmethod
	def GetAlias():  
		"""Return specified alias or if none the alias associated with the provided credentials."""
		if not clc._ALIAS:  Account.GetAccounts()
		return(clc._ALIAS)


	@staticmethod
	def GetLocation():  
		"""Return specified location or if none the default location associated with the provided credentials and alias."""
		if not clc._LOCATION:  Account.GetAccounts()
		return(clc._LOCATION)


	@staticmethod
	def GetAccountDetails(alias):
		"""Return account details dict associated with the provided alias."""
		r = clc.API.v1_call('post','Account/GetAccountDetails',{'AccountAlias': alias})
		if r['Success'] != True: 
			if clc.args:  clc.output.Status('ERROR',3,'Error calling %s.   Status code %s.  %s' % ('Account/GetAccountDetails',r['StatusCode'],r['Message']))
			raise Exception('Error calling %s.   Status code %s.  %s' % ('Account/GetAccountDetails',r['StatusCode'],r['Message']))
		elif int(r['StatusCode']) == 0:  
			r['AccountDetails']['Status'] = Account.account_status_itos[r['AccountDetails']['Status']]
			return(r['AccountDetails'])


	@staticmethod
	def GetLocations():
		"""Return all cloud locations available to the calling alias."""
		r = clc.API.v1_call('post','Account/GetLocations',{})
		if r['Success'] != True: 
			if clc.args:  clc.output.Status('ERROR',3,'Error calling %s.   Status code %s.  %s' % ('Account/GetLocations',r['StatusCode'],r['Message']))
			raise Exception('Error calling %s.   Status code %s.  %s' % ('Account/GetLocations',r['StatusCode'],r['Message']))
		elif int(r['StatusCode']) == 0:  
			clc.LOCATIONS = [x['Alias'] for x in r['Locations']]
			return(r['Locations'])


	@staticmethod
	def GetAccounts(alias=None):
		"""Return account inventory dict containing all subaccounts for the given alias.  If None search from default alias."""
		if alias is not None:  payload = {'AccountAlias': alias}
		else:  payload = {}
		r = clc.API.v1_call('post','Account/GetAccounts',payload)
		if int(r['StatusCode']) == 0:  
			# Assume first response is always the original account.  Not sure if this is reliable
			if not clc._ALIAS:  clc._ALIAS = r['Accounts'][0]['AccountAlias']
			if not clc._LOCATION:  clc._LOCATION = r['Accounts'][0]['Location']

			return(r['Accounts'])


