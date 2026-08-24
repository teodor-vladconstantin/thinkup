class Mentor extends Student {
  /**
   * Inherits Student class, with additional permissions, designed for each Team's Mentor
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
