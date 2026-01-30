class Tech extends Student {
  /**
   * Inherits Student Class, with the highest position in the role's hierarchy
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
