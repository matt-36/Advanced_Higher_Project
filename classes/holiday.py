class Holiday:
  """
  `Holiday` represents the general information which is not included within provider specific URL builder functions.
  """
  def __init__(self, ) -> None:
    ...

  def get_provider(self) -> str:
    t = type(self)
    return t