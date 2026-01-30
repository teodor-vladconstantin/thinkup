class Student {
  /**
   * Lowest Class in the hierarchy, designed for everyone joining ThinkUp
   * @param {String} name
   * @param {String} email
   * @param {Settings} settings
   * @param {Permissions} perms
   */

  constructor(name, email, settings, perms) {
    this.name = name;
    this.email = email;
    this.settings = settings;
    this.perms = perms;
  }

  getName() {
    return this.name;
  }

  setName(newName) {
    this.name = newName;
  }

  getSettings() {
    return this.settings;
  }

  setSettings(newSettings) {
    this.settings = newSettings;
  }

  getPerms() {
    return this.perms;
  }
}

// student --- name, email, image profile, settings class

/* student - competitor - mentor - tech
     |
    sponsor
*/
