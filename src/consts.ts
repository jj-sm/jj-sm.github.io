import type { Site, Page, Links, Socials } from "@types"

// Global
export const SITE: Site = {
  TITLE: "Juan José S. M.",
  DESCRIPTION: "Welcome to Astro Sphere, a portfolio and blog for designers and developers.",
  AUTHOR: "Mark Horn",
}

// Work Page
export const WORK: Page = {
  TITLE: "Work",
  DESCRIPTION: "Places I have worked.",
}

// export const ABOUT: Page = {
//   TITLE: "About",
//   DESCRIPTION: "Learn more about me.",
// }

// export const CODE: Page = {
//   TITLE: "Code",
//   DESCRIPTION: "Learn more about me.",
// }

// export const RESEARCH: Page = {
//   TITLE: "Research",
//   DESCRIPTION: "Learn more about me.",
// }

// export const CONTACT: Page = {
//   TITLE: "Research",
//   DESCRIPTION: "Learn more about me.",
// }

// Blog Page
export const BLOG: Page = {
  TITLE: "Blog",
  DESCRIPTION: "Writing on topics I am passionate about.",
}

// Projects Page 
export const PROJECTS: Page = {
  TITLE: "Projects",
  DESCRIPTION: "Recent projects I have worked on.",
}

// Search Page
export const SEARCH: Page = {
  TITLE: "Search",
  DESCRIPTION: "Search all posts and projects by keyword.",
}

// Links
export const LINKS: Links = [
  { 
    TEXT: "Home", 
    HREF: "/", 
  }
  // { 
  //   TEXT: "Work", 
  //   HREF: "/work", 
  // },
  // { 
  //   TEXT: "Blog", 
  //   HREF: "/blog", 
  // },
  // { 
  //   TEXT: "Projects", 
  //   HREF: "/projects", 
  // },
]

// Socials
export const SOCIALS: Socials = [
  { 
    NAME: "Email",
    ICON: "email", 
    TEXT: "iCloud Mail",
    HREF: "mailto:8-feta-scrawls@icloud.com",
  },
  { 
    NAME: "Github",
    ICON: "github",
    TEXT: "jj-sm",
    HREF: "https://github.com/jj-sm"
  },
  { 
    NAME: "LinkedIn",
    ICON: "linkedin",
    TEXT: "jj-sm",
    HREF: "https://www.linkedin.com/in/jj-sm/",
  },
  { 
    NAME: "Orcid",
    ICON: "orcid",
    TEXT: "0009-0005-4685-695X",
    HREF: "https://orcid.org/0009-0005-4685-695X",
  },
]

