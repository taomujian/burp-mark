from burp import IBurpExtender, IHttpListener
from burp import IContextMenuFactory, ITab
from java.io import PrintWriter
from javax.swing import JPanel, JTextField, JLabel, JButton
from java.awt import BorderLayout

class BurpExtender(IBurpExtender, IHttpListener, IContextMenuFactory, ITab):
  def registerExtenderCallbacks(self, callbacks):
    self._callbacks = callbacks
    self._helpers = callbacks.getHelpers()
    self._callbacks.setExtensionName("URL Highlighter")
    
    # Output and error streams for logging
    self.stdout = PrintWriter(callbacks.getStdout(), True)
    self.stderr = PrintWriter(callbacks.getStderr(), True)

    # Add this class as an HTTP listener
    self._callbacks.registerHttpListener(self)

    # Create and add a tab for user configuration (if needed)
    self.tabPanel = JPanel(BorderLayout())
    self.label = JLabel("Specify keyword to match in URLs:")
    self.textField = JTextField(20)
    # self.applyButton = JButton("Apply", actionPerformed=self.applySettings)

    panel = JPanel()
    panel.add(self.label)
    panel.add(self.textField)
    # panel.add(self.applyButton)
    self.tabPanel.add(panel, BorderLayout.NORTH)
    
    self._callbacks.addSuiteTab(self)

    # Initialize default keyword
    self.keyword_list = [line.strip() for line in open('keyword.txt', 'r').readlines()]
    self.stdout.println("URL Highlighter plugin loaded.")

  def getTabCaption(self):
    return "URL Highlighter"

  def getUiComponent(self):
    return self.tabPanel

  def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
    # Only process responses
    if not messageIsRequest:
      response = messageInfo.getResponse()
      requestInfo = self._helpers.analyzeRequest(messageInfo)

      # Get the URL from the request
      url = requestInfo.getUrl()
      for keyword in self.keyword_list:
        if keyword in str(url):
          messageInfo.setHighlight("red")
          self.stdout.println("Highlighted URL: {}".format(url))

