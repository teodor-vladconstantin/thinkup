class Sponsor extends Student {
  /**
   * Inherits Student Fields and Methods, designed for each Team's Sponsors
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

// atributii student +
