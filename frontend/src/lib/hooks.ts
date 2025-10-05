import { useDispatch, useSelector, type TypedUseSelectorHook } from "react-redux";

import type { SupportedLocale } from "@/lib/i18n";
import type { AppDispatch, RootState } from "@/state/store";

export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
export const useLocale = (): SupportedLocale => useAppSelector((state) => state.session.locale);

