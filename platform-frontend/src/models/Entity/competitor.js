class Competitor extends Student {
  /**
   * Inherits Student Fields and Methods, with higher privileges, designed for the Participants of TechUp
   * @param {String} name
   * @param {String} email
   * @param {Settings} settings
   * @param {Permissions} perms
   */

  constructor(name, email, settings, perms) {
    super(name);
    super(email);
    super(settings);
    super(perms);
  }
}
