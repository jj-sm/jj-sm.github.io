import { formatDate } from "@lib/utils"
import type { CollectionEntry } from "astro:content"

type Props = {
  entry: CollectionEntry<"blog"> | CollectionEntry<"projects"> | CollectionEntry<"research">
  pill?: boolean
}

export default function ArrowCard({entry, pill}: Props) {
    let externalUrl: string | undefined = undefined;
    let externalLinkLabel: string | undefined = undefined;

    if (entry.collection === "research") {
        if ('url' in entry.data && entry.data.url) {
            externalUrl = entry.data.url;
            externalLinkLabel = entry.data.urltext || "View Publication"; // Use urltext, or a default like "View Publication"
        }
        else if ('paperUrl' in entry.data && entry.data.paperUrl) {
            externalUrl = entry.data.paperUrl;
            externalLinkLabel = "View Paper";
        }
        else if ('paperRepo' in entry.data && entry.data.paperRepo) {
            externalUrl = entry.data.paperRepo;
            externalLinkLabel = "View Paper Repo";
        }
    }
    // Enable and adapt for projects if needed
    // else if (entry.collection === "projects") {
    //     if ('demoUrl' in entry.data && entry.data.demoUrl) {
    //         externalUrl = entry.data.demoUrl;
    //         externalLinkLabel = "View Demo";
    //     } else if ('repoUrl' in entry.data && entry.data.repoUrl) {
    //         externalUrl = entry.data.repoUrl;
    //         externalLinkLabel = "View Repo";
    //     }
    // }

    return (
      <a href={`/${entry.collection}/${entry.slug}`} class="group p-4 gap-3 flex items-center border rounded-lg bg-white dark:bg-black hover:bg-gray-100 hover:dark:bg-gray-900 border-black/15 dark:border-white/20 transition-colors duration-300 ease-in-out">
        <div class="w-full group-hover:text-black group-hover:dark:text-white blend">
          <div class="flex flex-wrap items-center gap-2">
            {pill && (
              <div class="text-sm capitalize px-2 py-0.5 rounded-full border border-black/15 dark:border-white/25">
                {entry.collection === "blog" ? "post" : entry.collection === "research" ? "research" : "project"}
              </div>
            )}
            <div class="text-sm uppercase">
              {formatDate(entry.data.date)}
            </div>
          </div>

          <div class="font-semibold mt-3 text-black dark:text-white">
            {entry.data.title}
          </div>

          <div class="text-sm line-clamp-2 mt-1">
            {entry.data.summary}
          </div>

          <div class="flex justify-between items-baseline mt-2 gap-2">
            <ul class="flex flex-wrap gap-1">
              {entry.data.tags.map((tag: string) => (
                <li class="text-xs uppercase py-0.5 px-1 rounded bg-black/5 dark:bg-white/20 text-black/75 dark:text-white/75">
                  {tag}
                </li>
              ))}
            </ul>
            {externalUrl && (
              <a
                href={externalUrl}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()} // Prevents the main card link from navigating
                class="text-xs uppercase py-0.5 px-1 rounded bg-sky-600 dark:bg-sky-700 text-white hover:bg-sky-700 dark:hover:bg-sky-600 transition-colors no-underline whitespace-nowrap flex-shrink-0"
                aria-label={externalLinkLabel}
              >
                {externalLinkLabel || "Link"}
              </a>
            )}
          </div>
        </div>
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="stroke-current group-hover:stroke-black group-hover:dark:stroke-white">
          <line x1="5" y1="12" x2="19" y2="12" class="scale-x-0 group-hover:scale-x-100 translate-x-4 group-hover:translate-x-1 transition-all duration-300 ease-in-out" />
          <polyline points="12 5 19 12 12 19" class="translate-x-0 group-hover:translate-x-1 transition-all duration-300 ease-in-out" />
        </svg>
      </a>
   )
}