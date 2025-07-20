import { format } from "date-fns";

export function formatISODate(iso: string, template = "dd MMM yyyy HH:mm") {
  return format(new Date(iso), template);
}
